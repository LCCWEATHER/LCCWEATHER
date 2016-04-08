from app import db, ma
import datetime
import random


class Lectura(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    humedad = db.Column(db.Integer)
    luz = db.Column(db.Integer, default=random.randint(1, 100))
    calidadaire = db.Column(db.Integer, default=random.randint(1, 100))
    nitrogeno = db.Column(db.Integer, default=random.randint(1, 100))
    monoxido = db.Column(db.Integer, default=random.randint(1, 100))
    temperatura = db.Column(db.Integer)
    presion = db.Column(db.Integer)

    def __init__(self, temperatura=None, presion=None, humedad=None):
        self.temperatura = temperatura
        self.presion = presion
        self.humedad = humedad

    def __repr__(self):
        return '<User %r>' % (self.temperatura)


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    active = db.Column(db.Boolean, default=False)

    def __init__(self, text=None, active=False):
        self.text = text
        self.active = active


class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    """metodos requeridos por flask-login"""
    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


class LecturaSchema(ma.ModelSchema):
    class Meta:
        model = Lectura


class AlertSchema(ma.ModelSchema):
    class Meta:
        model = Alert


def init_db():
    Base.metadata.create_all(bind=engine)
