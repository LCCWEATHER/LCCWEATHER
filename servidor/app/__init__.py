from flask import Flask, request, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config.from_object('app.config')
login_manager = LoginManager(app)

bcrypt = Bcrypt()

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.servidor_clima.views import mod as moduloClima
app.register_blueprint(moduloClima)

login_manager.login_view = "servidor_clima.login"
login_manager.login_message = \
    'Por favor inicia session para accesar esta pagina'
