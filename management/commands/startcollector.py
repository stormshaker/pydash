from django.core.management import BaseCommand
from background_task.models import Task
from pydash import tasks

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Start collecting data from Aquarium sensors"

    # A command must define handle()
    def handle(self, *args, **options):
        # Delete any existing datacollector tasks
        Task.objects.filter(task_name__exact="pydash.tasks.datacollector").delete()

        # Create new collector task
        tasks.datacollector(repeat=60)
        self.stdout.write("Data collector scheduled to run every 60 seconds.")
