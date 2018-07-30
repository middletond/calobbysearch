from utils import http, scrape
from utils.arrays import flatten

DOMAIN = "https://leginfo.legislature.ca.gov"
URL = DOMAIN + "/faces/billSearchClient.xhtml"

AVAILABLE_SESSIONS = (
    "20172018",
    "20152016",
    "20132014",
    "20112012",
    "20092010",
    "20072008",
    "20052006",
    "20032004",
    "20012002",
    "19992000",
)

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
        "billSearchForm:bill_number": "",
        "billSearchForm:house": "Both",
        "billSearchForm:hiddenHouse": "",
        "billSearchForm:statuteYear": "",
        "billSearchForm:chapter_number": "",
        "billSearchForm:session_year": session,
        "billSearchForm:hiddenSessionYr": "",
        "billSearchForm:author": "All",
        "billSearchForm:law_code": "All",
        "billSearchForm:law_section_num": "",
        "billSearchForm:keyword": "",
        "billSearchForm:attrSearch": "Search",
        "javax.faces.ViewState": scrape.value(sesh, VIEWSTATE_VALUE),
    })
    return clean(scrape.rows(sesh, RESULTS, {
        "url": "td[1]/a/@href",
        "name": "td[1]/a/text()",
        "title": "td[2]/text()",
        "author": "td[3]/text()",
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
