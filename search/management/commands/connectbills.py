from lobbying.models import Activity
from search import queue
from utils.arrays import unique

from . import LobbySearchCommand

class Command(LobbySearchCommand):
    help = "Creates M2M connections between `Activity` and `Bill` instances."

    def handle(self, *args, **options):
        connected_act_count = 0
        connected_bill_count = 0

        self.header("Connecting all lobby activities with related bills...")
        if queue.is_available():
            acts, bills = queue.connect_to_bills()
        else:
            acts, bills = Activity.objects.connect_to_bills()

        if acts and bills:
            connected_act_count = len(acts)
            connected_bill_count = len(unique(bills))
            self.success("Done. Connected {} acts to {} bills.".format(
                connected_act_count,
                connected_bill_count,
            ))
        else:
            self.failure("Warning. No acts were connected to bills.")

        return self.outcome_to_string((connected_act_count, connected_bill_count))
