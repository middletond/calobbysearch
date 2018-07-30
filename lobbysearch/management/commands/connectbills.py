from django.core.management.base import BaseCommand, CommandError

from lobbysearch.models import Activity

class Command(BaseCommand):
    help = "Creates M2M connections between `Activity` and `Bill` instances."

    def output(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def output_error(self, msg):
        self.stdout.write(self.style.ERROR(msg))

    def handle(self, *args, **options):
        self.output("Connecting all lobby activities with related bills...")
        connected_acts, connected_bills = Activity.objects.connect_to_bills()
        if connected_acts and connected_bills:
            self.output("Done. Connected {} acts to {} bills.".format(
                len(connected_acts),
                len(list(set(connected_bills))),
            ))
        else:
            self.output_error("Warning. No acts were connected to bills.")
