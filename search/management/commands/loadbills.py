import sys

from bills.models import Bill
from search import queue

from . import LobbySearchCommand

class Command(LobbySearchCommand):
    help = "Load canonical bill data from leginfo.legislature.gov into Bill model."

    def handle(self, *args, **options):
        loaded_bill_count = 0

        self.header("Fetching latest bill records from state website...")
        if queue.is_available():
            recs = queue.fetch_bills()
        else:
            recs = Bill.objects.fetch()

        if not recs:
            self.failure("Warning. No bill records were fetched.")
            sys.exit(1)
        else:
            self.output("Done. {} records fetched.".format(len(recs)))

        self.header("Loading bills into app using fetched records...")
        bills = Bill.objects.load(recs, clear_existing=True)

        if not bills:
            self.failure("Warning. No new bills were created.")
            sys.exit(1)
        else:
            loaded_bill_count = len(bills)
            self.success("Complete! {} new bills created.".format(loaded_bill_count))

        return self.outcome_to_string(loaded_bill_count)
