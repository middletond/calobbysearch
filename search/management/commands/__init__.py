from django.core.management.base import BaseCommand
from django.utils.termcolors import colorize

class LobbySearchCommand(BaseCommand):

    def header(self, msg):
        self.stdout.write(colorize(msg, fg="cyan", opts=("bold",)))

    def output(self, msg):
        self.stdout.write(colorize(msg, fg="white"))

    def success(self, msg):
        self.stdout.write(colorize(msg, fg="green", opts=("bold",)))

    def failure(self, msg):
        self.stdout.write(colorize(msg, fg="red", opts=("bold",)))
