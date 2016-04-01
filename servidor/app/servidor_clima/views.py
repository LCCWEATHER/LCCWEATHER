from flask import (Blueprint, render_template, abort, request, redirect,
                   current_app, redirect, url_for, flash)
from .forms import LoginForm, AddAlertForm
from .models import User, Alert
from flask.ext.login import (login_required, login_user, logout_user,
                             current_user)
from app import db, login_manager

mod = Blueprint('servidor_clima', __name__)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


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
                    flash("Limite de alertas activas ya esta alcanzado", "error")
    return render_template('editar_alerta.html', form=form, texto="Agregar alerta")


@mod.route('/modificar_alerta/<alert_id>', methods=["GET", "POST"])
@login_required
def edit_alert(alert_id):
    form = AddAlertForm()
    alert = Alert.query.get(alert_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            alert.text = form.text.data
            alert.active = form.active.data
            db.session.commit()
            return redirect(url_for('.alert_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash("Limite de alertas activas ya esta alcanzado", "error")
    form.text.data = alert.text
    return render_template(
        'editar_alerta.html',
         form=form,
         text="Modificar alerta",
         alert=alert.text
    )


@mod.route('/exportar', methods=["GET"])
@login_required
def export_data():
    return render_template('exportar.html')


@mod.route('/eliminar_alerta/<alert_id>', methods=["GET"])
@login_required
def delete_alert(alert_id):
    alert = Alert.query.get(alert_id);
    db.session.delete(alert)
    db.session.commit()
    return redirect(url_for('.alert_list'))


@mod.route('/toggle_alerta/<alert_id>', methods=["GET"])
@login_required
def toggle_alert(alert_id):
    alert = Alert.query.get(alert_id);

    if alert.active:
        alert.active = False
    elif Alert.query.filter(Alert.active).count() >= 3:
        flash("Ya esta seleccionado el maximo de alertas activas", "error")
    else:
        alert.active = True
    db.session.add(alert)
    db.session.commit()
    return redirect(url_for('.alert_list'))
