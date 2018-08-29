from django.utils import timezone
from django.core import management

from scrape.leginfo import bill_names
from search.models import PopulationAttempt
from . import LobbySearchCommand

COMMAND_BEGAN = "began"
COMMAND_FINISHED = "finished"

class Command(LobbySearchCommand):
    help = "Master command to download, clean, load, and connect lobbying data and bills."

    def __init__(self, *args, **kwargs):
        self.step = 1
        self.began = timezone.now()
        self.attempt = PopulationAttempt.objects.create(began=self.began)

        return super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.announce_subcommand("Downloading, cleaning, and loading raw lobbying data from CAL-ACCESS.")
        self.call_subcommand("updatecalaccess", noinput=True)

        self.announce_subcommand("Loading filed lobby activities from CAL-ACCESS raw data.")
        self.call_subcommand("loadactivities")

        self.announce_subcommand("Loading all bills from {}.".format(bill_names.DOMAIN))
        self.call_subcommand("loadbills")

        self.announce_subcommand("Finding bill names in filed activities and connecting to loaded bills.")
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

    def announce_subcommand(self, message, time_estimate=None):
        self.header("")
        self.header("-----------")
        self.header("STEP {} OF 4".format(self.step))
        self.header(message + "")
        if time_estimate:
            self.header("Note: this takes about {}.".format(time_estimate))
        self.header("-----------")
        self.step += 1
