from django.db import models

class Measurement(models.Model):
    date = models.DateTimeField("Measurement Date")
    roomtemp = models.DecimalField("Room Temperature", max_digits=4, decimal_places=2)
    roomhumidity = models.DecimalField("Room Humidity", max_digits=4, decimal_places=2)
    watertemp = models.DecimalField("Water Temperature", max_digits=4, decimal_places=2)
    ph = models.DecimalField("Water pH", max_digits=4, decimal_places=2)

    class Meta:
        get_latest_by = 'date'

class Aquarium(models.Model):
    frontlight = models.BooleanField("Front Light On")
    rearlight = models.BooleanField("Rear Light On")
    circpump = models.BooleanField("Circulation Pump On")
    co2 = models.BooleanField("CO2 On")
    filter = models.BooleanField("Filter On")
    accent = models.BooleanField("LED Accent Light On")

    def _get_last_water_temperature(self):
        m = Measurement.objects.latest()
        return m.watertemp

    def _get_last_room_temperature(self):
        m = Measurement.objects.latest()
        return m.roomtemp

    def _get_last_roomhumidity(self):
        m = Measurement.objects.latest()
        return m.roomhumidity

    def _get_last_ph(self):
        m = Measurement.objects.latest()
        return m.ph

    def get_daily_average_water_temp(date_from, date_to):
        m1 = Measurement.objects.filter(date__gte=date_from)
        m2 = m1.exclude(date___lte=date_to)
        # iterate over (date_to-date_from).days
           # calculate average for day, add to resultant array
        # return resultant array

    def set_front_light_on(self):
        if (self.frontlight is False):
            a = ArduinoTree()
            a.digitalWrite(15, a.HIGH)
            self.frontlight=TRUE
            self.save()

    def set_front_light_off(self):
        if (self.frontlight):
            a = ArduinoTree()
            a.digitalWrite(15, a.LOW)
            self.frontlight=FALSE
            self.save()

    def lastupdated(self):
        m = Measurement.objects.latest()
        return m.date

    watertemp = property(_get_last_water_temperature)
    roomtemp = property(_get_last_room_temperature)
    roomhumidity = property(_get_last_roomhumidity)
    ph = property(_get_last_ph)

    def __str__ (self):
        return str(self.date)

