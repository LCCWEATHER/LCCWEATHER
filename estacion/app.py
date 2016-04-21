import json
import requests
main():
    data={temperatura=(int)(random.random()*20),
                    concentracionCO=(int)(random.random()*57),
                    tiempo=datetime.datetime.now(),
                    presion=(int)(random.random()*43),
                    uv=(int)(random.random()*73),
                    humedad=(int)(random.random()*82),
                    intensidadLuz=(int)(random.random()*43),
                    calidadAire="Buena",
                    concentracionNO2=(int)(random.random()*42)
        }
    dataJson = json.dumps(data)
    r = requests.post("LINK A PAGINA", dataJson,auth=HTTPBasicAuth('usuario','contrasena'))
    r.text
if __name__ == '__main__':
    while true:
      threading.Timer(5.0, printit).start()
      main()
