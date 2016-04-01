from flask import Flask, render_template, jsonify
import random
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return funcionAuxiliar()

if __name__ == '__main__':
    app.run(debug=True, host='')

def get_newest_data():
    return jsonify(temperatura=g.data.temperatura,
                   concentracionCO=g.data.concentracionCO,
                   tiempo=g.data.tiempo, 
                   presion=g.data.presion,
                   uv=g.data.uv,
                   humedad=g.data.humedad,
                   intensidadLuz=g.data.intensidadLuz,
                   calidadAire=g.data.calidadAire,
                   concentracionNO2=g.data.concentracionNO2
                   )

def funcionAuxiliar():#todavia no hay componentes para calar esto pero pues en lo que sale
  return jsonify(temperatura=(int)(random.random()*20),
                   concentracionCO=(int)(random.random()*57),
                   tiempo=datetime.datetime.now(), 
                   presion=(int)(random.random()*43),
                   uv=(int)(random.random()*73),
                   humedad=(int)(random.random()*82),
                   intensidadLuz=(int)(random.random()*43),
                   calidadAire="Buena",
                   concentracionNO2=(int)(random.random()*42)
                   )