from django.utils import timezone
from django.core.management import call_command

from scrape.leginfo import bill_names
from search.models.records import PopulationAttempt, COMMAND_BEGAN
from . import LobbySearchCommand

class Command(LobbySearchCommand):
    help = "Master command to download, clean, load, and connect lobbying data and bills."

    def __init__(self, *args, **kwargs):
        self.step = 1
        self.attempt = PopulationAttempt()
        self.attempt.begin()

        return super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_true",
            dest="noinput",
            default=False,
            help="Run CAL-ACCESS update without asking permission"
        )

    def handle(self, *args, **options):
        self.noinput = options["noinput"]

        self.announce_subcommand("Downloading, cleaning, and loading raw lobbying data from CAL-ACCESS.")
        self.call_subcommand("updatecalaccess", noinput=self.noinput)

        self.announce_subcommand("Loading filed lobby activities from CAL-ACCESS raw data.")
        self.call_subcommand("loadactivities")

        self.announce_subcommand("Loading all bills from {}.".format(bill_names.DOMAIN))
        self.call_subcommand("loadbills")

        self.announce_subcommand("Finding bill names in filed activities and connecting to loaded bills.")
        self.call_subcommand("connectbills")

        self.output("Loading complete. Ready for searching!")

        self.attempt.finish(notify=True)

    def call_subcommand(self, command, *args, **kwargs):
        try:
            self.attempt.log(command, COMMAND_BEGAN)
            outcome = self.outcome_from_string(
                call_command(command, *args, **kwargs)
            )
            self.attempt.log_success(command, outcome)
        except Exception as error:
            self.attempt.log_failure(command, error)
            self.failure("Warning! This step not completed because of error: {}".format(error))

    def announce_subcommand(self, message):
        self.header("")
        self.header("-----------")
        self.header("STEP {} OF 4".format(self.step))
        self.header(message + "")
        self.header("-----------")
        self.header("")
        self.step += 1
