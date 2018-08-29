from django.utils import timezone
from django.core import management

from scrape.leginfo import bill_names
from search.models import LoadAttempt
from . import LobbySearchCommand

COMMAND_BEGAN = "began"
COMMAND_FINISHED = "finished"

class Command(LobbySearchCommand):
    help = "Master command to download, clean, load, and connect lobbying data and bills."

    def __init__(self, *args, **kwargs):
        self.step = 1
        self.began = timezone.now()
        self.finished = None
        self.attempt = LoadAttempt.objects.create(began=self.began)

        return super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.header("Downloading, cleaning, and loading raw lobbying data from CAL-ACCESS.")
        self.call_subcommand("updatecalaccess", noinput=True)

        self.header("Loading filed lobby activities from CAL-ACCESS raw data.")
        self.call_subcommand("loadactivities")

        self.header("Loading all bills from {}.".format(bill_names.DOMAIN))
        self.call_subcommand("loadbills")

        self.header("Finding bill names in filed activities and connecting to loaded bills.")
        self.call_subcommand("connectbills")

        self.output("Loading complete. Ready for searching!")

        self.attempt.finished = timezone.now()
        self.attempt.save()

    def call_subcommand(self, command, *args, **kwargs):
        self.update_attempt(command, COMMAND_BEGAN)
        management.call_command(command, *args, **kwargs)
        self.update_attempt(command, COMMAND_FINISHED)

    def update_attempt(self, command, event):
        field_to_update = "{}_{}".format(command, event)
        if hasattr(self.attempt, field_to_update):
            setattr(self.attempt, field_to_update, timezone.now())
            self.attempt.save()

    def header(self, message, time_estimate=None):
        header = "\n"
        header += "-----------\n"
        header += "STEP {} OF 4\n".format(self.step)
        header += message + "\n"
        if time_estimate:
            header += "Note: this takes about {}.\n".format(time_estimate)
        header += "-----------\n"
        self.output(header)
        self.step += 1
