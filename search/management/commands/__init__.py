from django.core.management.base import BaseCommand
from django.utils.termcolors import colorize

OUTCOME_DELIMITER = " " # outcome should only be integers

class LobbySearchCommand(BaseCommand):

    def header(self, msg):
        self.stdout.write(colorize(msg, fg="cyan", opts=("bold",)))

    def output(self, msg):
        self.stdout.write(colorize(msg, fg="white"))

    def success(self, msg):
        self.stdout.write(colorize(msg, fg="green", opts=("bold",)))

    def failure(self, msg):
        self.stdout.write(colorize(msg, fg="red", opts=("bold",)))

    def outcome_to_string(self, outcome):
        """Django only allows commands to output as strings."""
        if not outcome: return outcome # django ignores outcomes that resolve to false

        if isinstance(outcome, (tuple, list)):
            return OUTCOME_DELIMITER.join(str(val) for val in outcome)
        return str(outcome)

    def outcome_from_string(self, string):
        """And back again."""
        if not string: return string

        if OUTCOME_DELIMITER in string:
            return tuple(string.split())
        return int(string)
