from flask import (Blueprint, render_template, abort, request, redirect,
                   current_app, redirect, url_for, flash, jsonify, send_file, after_this_request)
from .forms import LoginForm, AddAlertForm
from .models import User, Alert, Lectura, LecturaSchema, AlertSchema
from flask.ext.login import (login_required, login_user, logout_user,
                             current_user)
from app import db, login_manager, bcrypt
import datetime
import csv
import tempfile
import os

mod = Blueprint('servidor_clima', __name__)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@login_manager.request_loader
def request_loader(request):
    auth = request.authorization
    if auth:
        user = User.query.filter_by(username=auth['username']).first()
        if user and bcrypt.check_password_hash(user.password, auth['password']):
            return user
    return None


@mod.route('/')
def index():
    return redirect(url_for('static', filename='visualizacion/index.html'))

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
        d = request.args.get('d')
        h = request.args.get('h')
        
        if h:
            h = float(h)
            now = datetime.datetime.utcnow() - datetime.timedelta(seconds=h / 1000.0)
            lecturas = Lectura.query \
                .filter(Lectura.fecha >= now) \
                .order_by(Lectura.fecha.desc())

        else:
            if not n and not d:
                n = 1
            if d:
                d = datetime.datetime.utcfromtimestamp(float(d)/1000.0)
                print(d.minute)
                lecturas = Lectura.query.filter(Lectura.fecha >= d).order_by(Lectura.fecha.desc())
            else:
                lecturas = Lectura.query.order_by(Lectura.fecha.desc())
        if n:
            lecturas = lecturas[:n]
        result = lecturas_schema.dump(lecturas)
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


@mod.route('/api/data.csv', methods=['GET'])
def csv_export():
    inferior = request.args.get('i')
    superior = request.args.get('s')

    if not inferior or not superior:
        abort(400)

    inferior = datetime.datetime.utcfromtimestamp(float(inferior) / 1000.0)
    superior = datetime.datetime.utcfromtimestamp(float(superior) / 1000.0)

    data = Lectura.query \
        .filter(Lectura.fecha >= inferior) \
        .filter(Lectura.fecha <= superior) \
        .order_by(Lectura.fecha.desc())

    data = lecturas_schema.dump(data)

    # handle, filepath = tempfile.mkstemp()

    csv_file = tempfile.TemporaryFile(mode='w+b')
    keys = ['id', 'fecha', 'humedad', 'luz', 'calidadaire', 'nitrogeno',
            'monoxido', 'temperatura', 'presion']


    #writer = csv.writer(csv_file)
    xd = str.encode(keys[0])
    csv_file.write(str.encode(','.join([key for key in keys])))
    csv_file.write(b'\n')

    for row in data.data:
        csv_file.write(str.encode(','.join([str(row[key]) for key in keys])  + '\n'))

    
    csv_file.seek(0)

    return send_file(csv_file, as_attachment=True, attachment_filename='data.csv')




@mod.route('/api/alertas', methods=['GET'])
def get_alertas():
    alerts = Alert.query.filter(Alert.active)
    result = alerts_schema.dump(alerts)
    print(result.data)
    return jsonify({'alertas': result.data})
