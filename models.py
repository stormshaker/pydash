from django.db import models

class Measurement(models.Model):
	date = models.DateTimeField()
	roomtemp = models.DecimalField(max_digits=4, decimal_places=2)
	roomhumidity = models.DecimalField(max_digits=4, decimal_places=2)
	watertemp = models.DecimalField(max_digits=4, decimal_places=2)
	ph = models.DecimalField(max_digits=4, decimal_places=2)

	def __str__ (self):
		return self.title


