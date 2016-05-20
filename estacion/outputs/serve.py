import json
import requests
import output

class Serve(output.Output()):
	def __init__(self,data):
		pass
	def outputData(self,dataPoints):
		for i in dataPoints:
			if i["name"]=="humidity":
				hum=i["value"]
			if i["name"]=="temperature":
				temp=i["value"]
		    data={temperatura=temp,humedad=hum}
    	dataJson = json.dumps(data)
		r=requests.post("148.225.71.4/api/lecturas",dataJson,auth=HTTPBasicAuth("admin","pingyburrito123")
		r.text
