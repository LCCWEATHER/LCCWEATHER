from flask_wtf import Form, validators
from wtforms import TextField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from app import db, bcrypt
from .models import User, Alert


def validate_login(form, field):
    user = form.get_user()

    if user is None:
        raise validators.ValidationError('Usuario invalido')
    if not bcrypt.check_password_hash(user.password, form.password.data):
        raise validators.ValidationError('Contraseña invalida')


def validate_active(form, field):
    q = Alert.query.filter(Alert.active)
    a = form.get_alert() if form.id.data else None

    if field.data and q.count() >= 3 and (a is None or not a.active):
        raise validators.ValidationError('Demasiadas alertas activas')


class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[
        DataRequired(), validate_login
    ])

    def get_user(self):
        return User.query.get(self.username.data)


class AddAlertForm(Form):
    id = IntegerField()
    text = TextField('text', validators=[DataRequired()])
    active = BooleanField(validators=[validate_active])

    def get_alert(self):
        return Alert.query.get(self.id.data)
