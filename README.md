# California Lobby Search by Bill
A public data search API that connects bills with lobbying activities in the California state legislature.

## But Why?

Every three months, lobbying activity is filed by both lobbyers (Form 625) and employers (Form 635). In the original filings, the entity data gets stored in different fields depending on which of these is filing. For example, when an employer files, the employer's address ends up under the fields meant for the hired lobby firm!

The purpose of this app is to:

1. connect basic filer information with the meaningful activity fields (payments, dates, employer interests), which in their original form exist in balkanized tables in the CAL-ACCESS data.
2. normalize these fields so they are always consistent and intuitive, regardless of who the original filer was.

By doing this, it can provide this basic picture of lobby activity:

employer ->
paid amount ->
to lobbyer ->
to influence interests / bills ->
during these dates

## Installation
Installation has been tested on Ubuntu 16.04. To install, do the following:

Install and setup all required services:

`$ bash deploy/setup.sh`

Deploy django to database and start up everything:

`$ bash deploy/app.sh`

To restart the app:

`$ bash deploy/restart.sh`

## Loading the Data
To load and connect the public data utilized by the app, run:

`$ python manage.py loadlobbysearch`

This will do the following:

1. Import the latest raw lobbying data from the California Secretary of State (SOS) [Cal-Access website](http://cal-access.sos.ca.gov/Lobbying/) via the installed `calaccess_raw` django app, created by the [California Civic Data Coalition](https://www.californiacivicdata.org/).
2. Connect the lobby activity fields scattered across different tables and load them into a new filed activities table.
3. Scrape the latest list of California bills from [leginfo.legislature.ca.gov](https://leginfo.legislature.ca.gov) and load it into a bills table.
4. Parse the bill names from filed activities and connect each filing to the loaded bills.

There is a discreet django management command available for each of these steps.
