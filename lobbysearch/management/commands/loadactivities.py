from django.core.management.base import BaseCommand, CommandError
from django.db import connection as django_connection

from lobbysearch.management import sql
from lobbysearch.models import Activity

class Command(BaseCommand):
    help = "Load CAL-ACCESS raw data into lobbysearch Activity model."

    def output(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def output_error(self, msg):
        self.stdout.write(self.style.ERROR(msg))

    def handle(self, *args, **options):
        with django_connection.cursor() as cursor:
            insert_count = 0

            prev_acts = Activity.objects.all()
            self.output("Clearing {} previous activities.".format(prev_acts.count()))
            prev_acts.delete()
            self.output("Done. All cleared.")
            self.output("")

            self.output("Loading activities filed by lobbyers from CAL-ACCESS tables...")
            cursor.execute(sql.LOAD_LOBBYER_ACTIVITIES)

            lobbyers_inserted = sql.inserted_rows(cursor)
            insert_count += lobbyers_inserted
            self.output("Done. {} lobbyer activities loaded.".format(lobbyers_inserted))
            self.output("")

            self.output("Loading activities filed by employers from CAL-ACCESS tables...")
            cursor.execute(sql.LOAD_EMPLOYER_ACTIVITIES)

            employers_inserted = sql.inserted_rows(cursor)
            insert_count += employers_inserted
            self.output("Done. {} employer activities loaded.".format(employers_inserted))
            self.output("")

        if insert_count:
            self.output("Complete. {} total activities loaded.".format(insert_count))
        else:
            self.output_error("WARNING: no new activities were loaded.")
