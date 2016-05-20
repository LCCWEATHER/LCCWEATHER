import json
import requests
import output

class Serve(output.Output()):
	def __init__(self,data):
		pass
	def outputData(self,dataPoints):
		dataJson=json.dumpsdataPoints)
		r=requests.post("148.225.71.4/api/lecturas",dataJson,auth=HTTPBasicAuth("admin","pingyburrito123")
		r.text
