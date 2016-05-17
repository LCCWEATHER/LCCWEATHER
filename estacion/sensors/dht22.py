import sensor
import dhtreader
import time
class DHT(sensor.Sensor):
    data=["measure","pin"]
    def __init__(self,data):
        dhtreader.init()
        dhtreader.lastDataTime = 0
        dhtreader.lastData = (None,None)
        self.name="DHT"
        self.pin = int(data["pin"])
        if "temp" in data["measure"].lower():
            self.dataName = "temperature"
            self.dataUnit = "Celsius"
            self.dataSymbol = "C"
        elif "h" in data["measure"].lower():
            self.dataName = "humidity"
            self.dataSimbol = "%"
            self.dataUnit = "%Relative humidity "
        return

    def getVal(self):
        tm = dhtreader.lastDataTime
		if (time.time()-tm)<2:
			t, h = dhtreader.lastData
		else:
			tim = time.time()
			try:
				t, h = dhtreader.read(22,self.pin)
			except Exception:
				t, h = dhtreader.lastData
			dhtreader.lastData = (t,h)
			dhtreader.lastDataTime=tim
		if self.dataName == "temperature":
			temp = t
			return temp
		elif self.dataName == "Relative_Humidity":
			return h
