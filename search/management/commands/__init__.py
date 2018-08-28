from django.core.management.base import BaseCommand

class LobbySearchCommand(BaseCommand):

    def output(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def output_error(self, msg):
        self.stdout.write(self.style.ERROR(msg))
