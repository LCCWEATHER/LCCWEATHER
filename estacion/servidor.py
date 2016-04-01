from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Servidor web LCC Weather'

if __name__ == '__main__':
    app.run(debug=True, host='')
def get_newest_data():#Sujeto a futuros cambios, esta funcion devuelve un objeto de tipo JSON
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