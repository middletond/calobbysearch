import requests

from .. import scrape


class Session(object):
    """Wrapper class to add browser-like behavior / interface to requests.Session.

    >>> from utils import http
    >>> sesh = http.Session()
    >>>
    >>> sesh.get('example.com/login/')
    >>> sesh.find('//input')
    [<InputElement ... name='username' type='text'>,
    <InputElement ... name='password' type='password'>]
    >>>
    >>> sesh.post('example.com/login/', {
    ...     'username': 'middletond',
    ...     'password': 'test1234'
    ... })
    """
    def __init__(self, *args, **kwargs):
        self._session = requests.Session(*args, **kwargs)
        self._response = None
        self.tree = None

    def full_url(self, url):
        return "http://" + url if not url.startswith("http") else url

    def get(self, url, params=None, **kwargs):
        self.response = self._session.get(self.full_url(url), params=params, **kwargs)

    def post(self, url, data=None, **kwargs):
        self.response = self._session.post(self.full_url(url), data=data, **kwargs)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self._response = response
        if response.text:
            if "html" in response.headers.get("content-type", ""):
                self.tree = scrape.tree_from_page(self.response, "html")
            elif "xml" in response.headers.get("content-type", ""):
                self.tree = scrape.tree_from_page(self.response, "xml")
            else:
                self.tree = None

    @property
    def url(self):
        return self.response.url if self.response else ''

    @property
    def page_source(self):
        return self.response.text if self.response else ''

    @property
    def page(self): # for convenience
        return self.page_source

    @property
    def cookies(self):
        return dict(self._session.cookies)

    @cookies.setter
    def cookies(self, cookies_dict):
        self._session.cookies.clear()
        if cookies_dict:
            requests.utils.add_dict_to_cookiejar(self._session.cookies, cookies_dict)

    @property
    def headers(self):
        return dict(self._session.headers)

    @headers.setter
    def headers(self, headers_dict):
        requests._session.headers = headers_dict

    @property
    def history(self):
        return self.response.history

    @property
    def was_redirected(self):
        return len(self.history) > 0

    def find(self, xpath, **kwargs):
        return self.tree.xpath(xpath, **kwargs)

    def exists(self, xpath, **kwargs):
        return bool(self.find(xpath, **kwargs))

    def elems(self):
        if not self.response:
            return []
        return [elem for elem in self.tree.iter()]
