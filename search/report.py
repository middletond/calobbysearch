"""Helper module for reporting app events to admins."""
from utils import slack

def search_ran(search):
    headline = "A new search has been run."
    url = search.get_admin_list_url()
    details = slack.attachment("details", {
        "Company": search.company,
        "Interest": search.interest,
        "Bill": search.bill,
        "Start Date": search.start,
        "End Date": search.end,
        "Session": search.session,
        "Amendments": "Latest Only" if search.latest_only else "All",
        "Result Count": search.result_count,
    }, url=url)
    return slack.message(headline, details)

def population_attempt_began(attempt):
    headline = "Population attempt #{} just began.".format(attempt.id)
    return slack.message(headline)

def population_attempt_finished(attempt):
    headline = "Population attempt #{} just finished.".format(attempt.id)
    url = attempt.get_admin_list_url()
    details = slack.attachment("details", {
        "Status": attempt.status,
        "Took": attempt.took(),
        "Began At": attempt.began,
        "Finished At": attempt.finished,
        "Updating Calaccess Took": attempt.updatecalaccess_took(),
        "Loading Activities Took": attempt.loadactivities_took(),
        "Loading Bills Took": attempt.loadbills_took(),
        "Connecting Bills Took": attempt.connectbills_took(),
        "Failures": attempt.reason,
    }, url=url)
    stats = slack.attachment("stats", {
        "Activities Loaded": attempt.loadactivities_count,
        "Bills Loaded": attempt.loadbills_count,
        "Activities Connected": attempt.connectedacts_count,
        "Bills Connected": attempt.connectedbills_count,
    }, url=url)
    return slack.message(headline, [details, stats])
