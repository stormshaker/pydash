from django.contrib import admin
from .models import Measurement

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('date', 'roomtemp', 'roomhumidity', 'watertemp', 'ph')

admin.site.register(Measurement,MeasurementAdmin) 
