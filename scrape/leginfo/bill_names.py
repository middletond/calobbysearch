from utils import http, scrape
from utils.arrays import flatten
from utils.session import Session

DOMAIN = "https://leginfo.legislature.ca.gov"
URL = DOMAIN + "/faces/billSearchClient.xhtml"

AVAILABLE_SESSIONS = Session.available_sessions()

def run():
    return flatten(crawl(session) for session in AVAILABLE_SESSIONS)

def crawl(session):
    VIEWSTATE_VALUE = "//input[@name='javax.faces.ViewState' and contains(@id, 'ViewState:0')]/@value"
    RESULTS = "//table[@id='bill_results']/tbody/tr"
    output(session)

    sesh = http.Session()
    # load the form page so we can scrape required `viewstate` value
    sesh.get(URL)
    # do the actual form submission
    sesh.post(URL, {
        "billSearchForm": "billSearchForm",
        "bill_number": "",
        "house": "Both",
        "hiddenHouse": "",
        "statuteYear": "",
        "chapter_number": "",
        "session_year": session,
        "hiddenSessionYr": "",
        "author": "All",
        "law_code": "All",
        "law_section_num": "",
        "keyword": "",
        "javax.faces.ViewState": scrape.value(sesh, VIEWSTATE_VALUE),
    })
    return clean(scrape.rows(sesh, RESULTS, {
        "url": "td[1]/a/@href",
        "name": "td[1]/a/text()",
        "title": "td[2]/text()",
        "authors": "td[3]/text()",
        "status": "td[4]/text()",
    }), session)

def clean(records, session):
    for row in records:
        row.update({
            "url": DOMAIN + row["url"],
            "session": session,
        })
    return records

def output(session):
    print("Scraping all {} bills from {}...".format(session, URL))
