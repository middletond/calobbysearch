from django.db import connection as django_connection

from lobbying.models import Activity
from search.management import sql

from . import LobbySearchCommand

class Command(LobbySearchCommand):
    help = "Load CAL-ACCESS raw data into lobbying Activity model."

    def handle(self, *args, **options):
        with django_connection.cursor() as cursor:
            insert_count = 0

            prev_acts = Activity.objects.all()
            self.header("Clearing {} previous activities.".format(prev_acts.count()))
            # prev_acts.delete()
            cursor.execute(sql.TRUNCATE_ACTIVITIES)
            self.output("Done. All cleared.")
            self.output("")

            self.header("Loading activities filed by lobby firms from CAL-ACCESS tables...")
            cursor.execute(sql.LOAD_LOBBYER_ACTIVITIES)

            acts_inserted = sql.inserted_rows(cursor)
            insert_count += acts_inserted
            self.output("Done. {} new activities loaded.".format(acts_inserted))
            self.output("")

            self.header("Loading contracted-firm activities filed by employers from CAL-ACCESS tables...")
            cursor.execute(sql.LOAD_EMPLOYER_ACTIVITIES_FIRMS)

            acts_inserted = sql.inserted_rows(cursor)
            insert_count += acts_inserted
            self.output("Done. {} new activities loaded.".format(acts_inserted))
            self.output("")

            self.header("Loading in-house activities filed by employers from CAL-ACCESS tables...")
            cursor.execute(sql.LOAD_EMPLOYER_ACTIVITIES_INHOUSE)

            acts_inserted = sql.inserted_rows(cursor)
            insert_count += acts_inserted
            self.output("Done. {} new activities loaded.".format(acts_inserted))
            self.output("")

            self.header("Loading other pay-to-influence activities filed by employers from CAL-ACCESS tables...")
            cursor.execute(sql.LOAD_EMPLOYER_ACTIVITIES_OTHER)

            acts_inserted = sql.inserted_rows(cursor)
            insert_count += acts_inserted
            self.output("Done. {} new activities loaded.".format(acts_inserted))
            self.output("")

        if insert_count:
            self.success("Loading complete! {} total activities loaded.".format(insert_count))
        else:
            self.failure("WARNING: no new activities were loaded.")

        return self.outcome_to_string(insert_count)
