# California Lobby Search by Bill
A public data search API that connects bills with lobbying activities in the California state legislature.

The what, why, and how is covered on [the about page](https://calobbysearch.org/about).

This is the backend of the app. There is also a [frontend](https://github.com/middletond/calobbysearch-frontend), which can be [tried out here](https://calobbysearch.org).

## Installation
Installation has been tested on Ubuntu 16.04. To install, do the following:

Install and setup all required services:

`$ bash deploy/setup.sh`

Deploy django to database and start up everything:

`$ bash deploy/app.sh`

To restart the app:

`$ bash deploy/restart.sh`

## Adding the Data
To load and connect the public data utilized by the app, run:

`$ python manage.py populate`

This will do the following:

1. Import the latest raw lobbying data from the California Secretary of State (SOS) [Cal-Access website](http://cal-access.sos.ca.gov/Lobbying/) via the installed `calaccess_raw` django app, created by the [California Civic Data Coalition](https://www.californiacivicdata.org/).
2. Connect the lobby activity fields scattered across different tables and load them into a new filed activities table.
3. Scrape the latest list of California bills from [leginfo.legislature.ca.gov](https://leginfo.legislature.ca.gov) and load it into a bills table.
4. Parse the bill names from filed activities and connect each filing to the loaded bills.

There is a discreet django management command available for each of these steps.
