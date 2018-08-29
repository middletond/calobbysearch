import sys

from bills.models import Bill
from search import queue

from . import LobbySearchCommand

class Command(LobbySearchCommand):
    help = "Load canonical bill data from leginfo.legislature.gov into Bill model."

    def handle(self, *args, **options):
        clear_existing = True # make this an arg

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
        bills = Bill.objects.load(recs, clear_existing=clear_existing)

        if not bills:
            self.failure("Warning. No new bills were created.")
            sys.exit(1)
        else:
            self.success("Complete! {} new bills created.".format(len(bills)))
