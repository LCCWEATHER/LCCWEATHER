from app.servidor_clima.models import Lectura
from app import db
import requests
import random

apikey = '9f7f4e7ce8bb9b072eba080ed7b9efd6'

params = {'q': 'Hermosillo', 'APPID': apikey}


def update():

    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params)
    json = r.json()
    l = Lectura(
        json['main']['temp'] + random.randint(-3, 3),
        json['main']['pressure'] + random.randint(-3, 3),
        json['main']['humidity'] + random.randint(-3, 3)
    )

    db.session.add(l)

    db.session.commit()

if(__name__ == '__main__'):
    update()
