from service import celery_app
from scrape import leginfo

from .models import Activity

@celery_app.task
def connect_to_bills(session):
    acts, bills = Activity.objects.connect_to_bills(session)
    return (
        [act.id for act in acts],
        [bill.id for bill in bills],
    )

@celery_app.task
def fetch_bills(session):
    # return [{'url': 'https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=201720180AB1', 'name': 'AB-1', 'title': 'Transportation funding.', 'authors': 'Frazier', 'status': 'Assembly - Died - Transportation', 'session': '20172018'}, {'url': 'https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=201720180AB2', 'name': 'AB-2', 'title': 'Hate crimes: peace officers.'}]
    return leginfo.bill_names.crawl(session)

@celery_app.task
def test(num):
    print("TESTING: {}".format(num))
    return num * 2
