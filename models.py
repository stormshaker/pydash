from django.db import models

class Measurement(models.Model):
	date = models.DateTimeField("Measurement Date")
	roomtemp = models.DecimalField("Room Temperature", max_digits=4, decimal_places=2)
	roomhumidity = models.DecimalField("Room Humidity", max_digits=4, decimal_places=2)
	watertemp = models.DecimalField("Water Temperature", max_digits=4, decimal_places=2)
	ph = models.DecimalField("Water pH", max_digits=4, decimal_places=2)

	def __str__ (self):
		return str(self.date)

