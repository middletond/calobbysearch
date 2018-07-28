from . import dates

SESSION_STRING_FORMAT = "{}{}"; # ex: "20172018"
EARLIEST_YEAR = 1999

class Session:
    """Small helper class to handle legislative sessions."""
    def __init__(self, sesh_string=None):
        if not sesh_string:
            sesh_string = Session.current_session_string()

        self.start_year = sesh_string[0:4]
        self.end_year = sesh_string[4:8]
        self.start_date = dates.parse(self.start_year)
        self.end_date = dates.parse("12/31/{}".format(self.end_year))

    def as_years(self):
        return (self.start_year, self.end_year)

    def as_dates(self):
        return (self.start_date, self.end_date)

    def as_string(self):
        return Session.string_from_dates(*self.as_years())

    @staticmethod
    def string_from_dates(start, end):
        return SESSION_STRING_FORMAT.format(start, end)

    @staticmethod
    def current_session_string():
        current_year = int(dates.today().strftime("%Y"))
        if current_year % 2 == 0: # even year, ex: 2018 -> 2017-2018 session
            start = current_year - 1
            end = current_year
        else:
            start = current_year # odd year, ex: 2017 -> 2017-2018 session
            end = current_year + 1
        return Session.string_from_dates(start, end)

    @staticmethod
    def available_choices():
        return (
            ("20172018", "2017 - 2018"),
        )
