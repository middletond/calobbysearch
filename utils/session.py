from . import dates

SESSION_STRING_FORMAT = "{}{}"; # ex: "20172018"
SESSION_STRING_FORMAT_VERBOSE = "{} - {}"
EARLIEST_YEAR = 1999

YEAR_ONLY_FORMAT = "%Y"

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
    def string_from_date(date):
        year = int(dates.format(date, YEAR_ONLY_FORMAT))
        if year % 2 == 0: # even year, ex: 2018 -> 2017-2018 session
            start = year - 1
            end = year
        else:
            start = year # odd year, ex: 2017 -> 2017-2018 session
            end = year + 1
        return SESSION_STRING_FORMAT.format(start, end)

    @staticmethod
    def current_session_string():
        return Session.string_from_dates(current_year())

    @staticmethod
    def available_sessions():
        start, end, increment = EARLIEST_YEAR, Session.current_year(), 2
        sesh_years = range(end, start, -increment) # DESC order
        return tuple(Session.string_from_date(year) for year in sesh_years)

    @staticmethod
    def available_choices():
        def to_choice(session):
            session_verbose = SESSION_STRING_FORMAT_VERBOSE.format(
                session[:4],
                session[4:8])
            return (session, session_verbose)
        return tuple(to_choice(session) for session in Session.available_sessions())

    @staticmethod
    def current_year():
        return int(dates.today().strftime(YEAR_ONLY_FORMAT))
