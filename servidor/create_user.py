from getpass import getpass
import sys

from flask import current_app
from app import app, bcrypt, db
from app.servidor_clima.models import User

def main():
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print('Ya existe un usuario. ¿Crear otro?')
            create = input()
            if create == 'n':
                return

        print('Nombre de usuario: ')
        username = input()
        password = getpass("Contraseña: ")
        assert password == getpass('Vuelve a introducir ontraseña: ')

        user = User(
            username=username,
            password=bcrypt.generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        print('usuario agregado')

if __name__ == '__main__':
    sys.exit(main())
