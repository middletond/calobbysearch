from service import celery_app
from scrape import leginfo

from lobbying.models import Activity

@celery_app.task
def connect_to_bills(session):
    acts, bills = Activity.objects.connect_to_bills(session)
    return (
        [act.id for act in acts],
        [bill.id for bill in bills],
    )

@celery_app.task
def fetch_bills(session):
    return leginfo.bill_names.crawl(session)

@celery_app.task
def test(num):
    print("TESTING: {}".format(num))
    return num * 2
