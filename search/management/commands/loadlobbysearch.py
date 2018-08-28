from django.core.management.base import BaseCommand
from django.core import management

from scrape.leginfo import bill_names

class Command(BaseCommand):
    help = "Master command to download, clean, load, and connect lobbying data and bills."

    def output(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def output_error(self, msg):
        self.stdout.write(self.style.ERROR(msg))

    def handle(self, *args, **kwargs):
        self.output("")
        self.output("-----------")
        self.output("STEP 1 OF 4")
        self.output("Downloading, cleaning, and loading raw lobbying data from CAL-ACCESS.")
        self.output("Note: this takes about an 20 mins.")
        self.output("-----------")
        management.call_command("updatecalaccess")

        self.output("")
        self.output("-----------")
        self.output("STEP 2 OF 4")
        self.output("Loading filed lobby activities from CAL-ACCESS raw data.")
        self.output("-----------")
        management.call_command("loadactivities")

        self.output("")
        self.output("-----------")
        self.output("STEP 3 OF 4")
        self.output("Loading all bills from {}.".format(bill_names.DOMAIN))
        self.output("-----------")
        management.call_command("loadbills")

        self.output("")
        self.output("-----------")
        self.output("STEP 4 OF 4")
        self.output("Parsing bill names from filed activities and connecting to loaded bills.")
        self.output("Note: this takes about an hour. Time for a good psoas stretch.")
        self.output("-----------")
        management.call_command("connectbills")

        self.output("Loading complete. Ready for searching!")
