from flask import (Blueprint, render_template, abort, request, redirect,
                   current_app, redirect, url_for, flash, jsonify)
from .forms import LoginForm, AddAlertForm
from .models import User, Alert, Lectura, LecturaSchema, AlertSchema
from flask.ext.login import (login_required, login_user, logout_user,
                             current_user)
from app import db, login_manager, bcrypt

mod = Blueprint('servidor_clima', __name__)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@login_manager.request_loader
def request_loader(request):
    auth = request.authorization
    user = User.query.filter_by(username=auth['username']).first()
    if user and bcrypt.check_password_hash(user.password, auth['password']):
        return user
    return None


@mod.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = form.get_user()
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for('.alert_list'))
        else:
            flash('Datos incorrectos', 'error')

    if current_user.is_authenticated:
        return redirect(url_for('.alert_list'))

    return render_template('login.html', form=form)


@mod.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('.login'))


@mod.route('/alertas', methods=["GET"])
@login_required
def alert_list():
    return render_template('alerts.html', data=Alert.query.all())


@mod.route('/agregar_alerta', methods=["GET", "POST"])
@login_required
def add_alert():
    form = AddAlertForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            alert = Alert(text=form.text.data, active=form.active.data)
            db.session.add(alert)
            db.session.commit()
            return redirect(url_for('.alert_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash("Limite de alertas activas ya esta alcanzado",
                          "error")
    return render_template(
        'edit_alert.html',
        form=form,
        header_text="Agregar alerta"
    )


@mod.route('/modificar_alerta/<alert_id>', methods=["GET", "POST"])
@login_required
def edit_alert(alert_id):
    form = AddAlertForm()
    alert = Alert.query.get(alert_id)
    form.id.data = alert.id
    if request.method == 'POST':
        if form.validate_on_submit():
            alert.text = form.text.data
            alert.active = form.active.data
            db.session.commit()
            return redirect(url_for('.alert_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash("Limite de alertas activas ya esta alcanzado",
                          "error")
    form.text.data = alert.text
    form.active.data = alert.active
    return render_template('edit_alert.html',
                           form=form,
                           header_text="Modificar alerta",
                           alert=alert.text)


@mod.route('/exportar', methods=["GET"])
@login_required
def export_data():
    return render_template('exportar.html')


@mod.route('/eliminar_alerta/<alert_id>')
@login_required
def delete_alert(alert_id):
    alert = Alert.query.get(alert_id)
    db.session.delete(alert)
    db.session.commit()
    return redirect(url_for('.alert_list'))


@mod.route('/toggle_alerta/<alert_id>', methods=["GET"])
@login_required
def toggle_alert(alert_id):
    alert = Alert.query.get(alert_id)

    if alert.active:
        alert.active = False
    elif Alert.query.filter(Alert.active).count() >= 3:
        flash("Ya esta seleccionado el maximo de alertas activas", "error")
    else:
        alert.active = True
    db.session.add(alert)
    db.session.commit()
    return redirect(url_for('.alert_list'))

lecturas_schema = LecturaSchema(many=True)
alerts_schema = AlertSchema(many=True)


@mod.route('/api/lecturas', methods=['GET', 'POST'])
def get_lecturas():
    if request.method == 'GET':
        n = request.args.get('n')

        if not n:
            n = 1
        lecturas = Lectura.query.order_by(Lectura.fecha.desc())[:n]
        result = lecturas_schema.dump(lecturas)
        print(result.data)
        return jsonify({'datos': result.data})
    if request.method == 'POST':
        print(current_user)
        if not current_user.is_authenticated():
            abort(403)
        data = request.get_json()
        try:
            l = Lectura(
                temperatura=data['temperatura'],
                presion=data['presion'],
                humedad=data['humedad']
            )
            db.session.add(l)
            db.session.commit()
            return jsonify({'status': 'sik'})
        except KeyError:
            abort(500)


@mod.route('/api/alertas')
def get_alertas():
    alerts = Alert.query.filter(Alert.active)
    result = alerts_schema.dump(alerts)
    print(result.data)
    return jsonify({'alertas': result.data})
