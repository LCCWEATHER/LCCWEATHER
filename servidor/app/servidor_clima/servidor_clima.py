import logging

from flask import (Flask, render_template, abort, request, redirect,
                   current_app, redirect, url_for)
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import (LoginManager, login_required, login_user,
                             logout_user, current_user)
from flask_restful import Resource, Api, reqparse

from .models import Lectura, User, db
from .forms import LoginForm

logger = logging.getLogger(__name__)
app = Flask(__name__)
login_manager = LoginManager()
api = Api(app)
bcrypt = Bcrypt()

login_manager

parser = reqparse.RequestParser()
parser.add_argument(
    'n',
    type=int,
    location='args',
    help='Especifica un numero entero'
)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class Lecturas(Resource):
    def get(self):
        args = parser.parse_args()

        n = 1
        if args['n']:
            n = args['n']

        print(n)

        q = db_session.query(Lectura).order_by(Lectura.fecha.desc())[:n]

        return {
            'lecturas': [{
                'temperatura': l.temperatura,
                'presion': l.presion,
                'humedad': l.humedad,
                'luz': l.luz,
                'calidadaire': l.calidadaire,
                'nitrogeno': l.nitrogeno,
                'monoxido': l.monoxido,
                'fecha': l.fecha.strftime("%H:%M:%S")
            } for l in q]
        }

api.add_resource(Lecturas, '/api/lectura')


if __name__ == '__main__':
    app.run(debug=True)
