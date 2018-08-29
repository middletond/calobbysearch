from lobbying.models import Activity
from search import queue

from . import LobbySearchCommand

class Command(LobbySearchCommand):
    help = "Creates M2M connections between `Activity` and `Bill` instances."

    def handle(self, *args, **options):
        self.output("Connecting all lobby activities with related bills...")

        if queue.is_available():
            acts, bills = queue.connect_to_bills()
        else:
            acts, bills = Activity.objects.connect_to_bills()

        if acts and bills:
            self.success("Done. Connected {} acts to {} bills.".format(
                len(acts),
                len(list(set(bills))),
            ))
        else:
            self.failure("Warning. No acts were connected to bills.")
