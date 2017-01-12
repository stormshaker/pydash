from django.apps import AppConfig
#from pydash import collector

class AquaPyDashConfig(AppConfig):
    name = 'pyDash'
    verbose_name = "AquaPy Aquarium Monitor/Controller"
    #def ready(self):
        #pydash.collector.datacollector(repeat=60) # startup code here