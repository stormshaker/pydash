# Collect monitor data from sensors and write to database
from nanpy import DHT
import time
import datetime
from pydash.models import Measurement
from background_task import background

@background(schedule=60)
def datacollector():

	dht = DHT(10,DHT.DHT11)

	while True:
	    """
	    Get temp and humidty from DHT 11 sensor on Arduino using nanpy
	    """
	    try:
	        temp = dht.readTemperature(False)
	        humid = dht.readHumidity()
	        measure = Measurement(date=datetime.datetime.now(), roomtemp=t, roomhumidity=humid, watertemp='0', ph='0')    
	        measure.save()

	    except Exception as err:
	        print(str(err))

