from django.contrib import admin
from .models import Measurement,Aquarium

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('date', 'roomtemp', 'roomhumidity', 'watertemp', 'ph')

class AquariumAdmin(admin.ModelAdmin):
    list_display = ('frontlight', 'rearlight', 'circpump', 'co2', 'filter', 'accent')

admin.site.register(Measurement,MeasurementAdmin)
admin.site.register(Aquarium,AquariumAdmin) 
