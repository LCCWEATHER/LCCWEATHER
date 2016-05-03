from app.servidor_clima.models import Lectura
from app import db
import requests
import random

apikey = '9f7f4e7ce8bb9b072eba080ed7b9efd6'

params = {'q': 'Hermosillo', 'APPID': apikey}


def update():
    l = Lectura(
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100)
    )

    db.session.add(l)

    db.session.commit()

if(__name__ == '__main__'):
    update()
