# Collect monitor data from sensors and write to database
from nanpy import DHT
from django.utils import timezone
from pydash.models import Measurement
from background_task import background

@background(schedule=10)
def datacollector():

    # TODO: Ensure only a single instance runs

    dht = DHT(10,DHT.DHT11)

    """
    Get temp and humidty from DHT 11 sensor on Arduino using nanpy
    """
    try:
        temp = dht.readTemperature(False)
        humid = dht.readHumidity()
        measure = Measurement(date=timezone.now(), roomtemp=temp, roomhumidity=humid, watertemp='0', ph='0')    
        measure.save()
        print("Data saved")

    except Exception as err:
        print(str(err))

    return "Collector Started"
