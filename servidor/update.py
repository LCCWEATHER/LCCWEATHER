from app.servidor_clima.models import Lectura
from app import db
import requests

apikey = '9f7f4e7ce8bb9b072eba080ed7b9efd6'

params = {'q': 'Hermosillo', 'APPID': apikey}


def update():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params)
    json = r.json()

    print(json)

    l = Lectura(
        json['main']['temp'],
        json['main']['pressure'],
        json['main']['humidity']
    )
    db.session.add(l)

    db.session.commit()
