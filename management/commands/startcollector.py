from django.core.management import BaseCommand
from pydash import tasks

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Start collecting data from Aquarium sensors"

    # A command must define handle()
    def handle(self, *args, **options):
    	tasks.datacollector(repeat=60)
    	self.stdout.write("Data collector scheduled to run every 60 seconds.")