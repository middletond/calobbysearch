"""Helpers for dates and times.

"""
import re

from datetime import timedelta
from dateutil.parser import parse as dateutil_parse
from django.utils import timezone


BEGINNING_OF_TIME = "1900/01/01"
YEAR_ONLY = r"^\d{4}$"


def today():
    """Datetime of today's date."""
    return timezone.now()


def timestamp(dformat='%Y-%m-%d'):
    """Simple formatted timestamp helper."""
    return timezone.now().strftime(dformat)


def parse(date_str, assume="start"):
    """A lazy version of dateutil string parse()"""
    if isinstance(date_str, int):
        date_str = str(date_str)
    if not isinstance(date_str, str):
        return date_str
    if re.match(YEAR_ONLY, date_str) and assume == "start":
        date_str = "01/01/{}".format(date_str)
    elif re.match(YEAR_ONLY, date_str) and assume == "end":
        date_str = "12/31/{}".format(date_str)
    return dateutil_parse(date_str)


def format(date, dformat):
    """Return a formatted date string from a date obj or string."""
    return parse(date).strftime(dformat)


def inclusive_range(start, end=None):
    """Converts date strings to datetime range up to the last minute of the end date.

       Used to make timestamp lookups from date strings."""
    if not end:
        end = start
    return (parse(start, assume="start").replace(hour=0, minute=0,
                                                 second=0, microsecond=0),
            parse(end, assume="end").replace(hour=23, minute=59,
                                             second=0, microsecond=0))


def humanize_delta(timedelta, decimal=None):
    """Returns short human-readable string for a timedelta object."""
    PER_MINUTE = 60
    PER_HOUR = 3600
    PER_DAY = 3600 * 24

    seconds = timedelta.seconds
    if seconds < PER_MINUTE:
        unit = "second"
        value = seconds
    elif seconds >= PER_MINUTE and seconds < PER_HOUR:
        unit = "minute"
        value = round(seconds / PER_MINUTE, decimal)
    elif seconds >= PER_HOUR and seconds < PER_DAY:
        unit = "hour"
        value = round(seconds / PER_HOUR, decimal)
    else:
        unit = "day"
        value = round(timedelta.days, decimal)

    if value != 1: unit += "s" # pluralize

    return "{} {}".format(value, unit)
