import functools
from urllib.parse import urlencode, urlparse

from selenium import webdriver
from selenium.webdriver.support.select import Select
import pyvirtualdisplay

from .download import Downloader
from service import settings as service_settings


#: Chrome browser type.
CHROME = 'chrome'
#: PhantomJS browser type.
PHANTOMJS = 'phantom'
# Use Chrome in test, phantom (headless) otherwise
TEST_MODE = service_settings.SCRAPING_TEST_MODE


class Browser(webdriver.Chrome, webdriver.PhantomJS):
    """
    Convenience wrapper to combine selenium webdrivers and simplify their API.
    """
    def __init__(self, browser_type=None, capture_downloads=False):
        self.running = True
        self.download_path = None

        if not browser_type:
            if TEST_MODE:
                browser_type = CHROME
            else:
                browser_type = PHANTOMJS
        self.browser_type = browser_type

        if self.browser_type == CHROME: # A display is required for Chrome on servers.
            if not TEST_MODE:
                self.display = pyvirtualdisplay.Display(visible=0, size=(1200, 800))
                self.display.start()

            options = webdriver.ChromeOptions()
            if capture_downloads:
                self.downloader = Downloader()
                prefs = {"download.default_directory" : self.downloader.path}
                options.add_experimental_option("prefs", prefs)

            webdriver.Chrome.__init__(self, chrome_options=options)
        else:
            args = []
            if capture_downloads:
                raise Exception('File downloading is not possible with PhantomJS.')
            webdriver.PhantomJS.__init__(self, service_args=args)
            self.set_window_size(1200, 800)

    def get(self, url, **params):
        """Go to the specified url. If params are specified, they are added to the URL as GET parameters."""
        if len(params) != 0:
            url = url + '?' + urlencode(params)
        super(Browser, self).get(url)

    def find(self, xpath):
        """Returns the element at the xpath. Throws an exception if the element doesn't exist."""
        return self.find_element_by_xpath(xpath)

    def exists(self, xpath):
        """Return whether an element exists at the xpath."""
        try:
            self.find(xpath)
            return True
        except:
            return False

    def click(self, xpath):
        """Click on the element at the xpath."""
        self.find_element_by_xpath(xpath).click()

    def input(self, text, xpath):
        """Input the specified string into the element at the xpath."""
        self.find_element_by_xpath(xpath).send_keys(text)

    def wait_for(self, xpath, timeout=150, displayed=False):
        """Wait for an element to exist at the xpath."""
        wait = webdriver.support.wait.WebDriverWait(self, timeout)
        if displayed:
            condition = lambda b: b.find_element_by_xpath(xpath).is_displayed()
        else:
            condition = lambda b: b.find_element_by_xpath(xpath)
        wait.until(condition)

    def select_option(self, xpath, value=None, text=None, index=None):
        """ Select an option from a dropdown / select element. """
        if len(list(filter(None, (value, text, index)))) != 1:
            raise ValueError("You must supply exactly one of (value, text, index) kwargs")
        select = Select(self.find(xpath))
        if value is not None:
            select.select_by_value(value)
        elif text is not None:
            select.select_by_visible_text(text)
        else:
            select.select_by_index(index)

    def get_cookies(self):
        """Return a dictionary of the cookies in the browser."""
        return {cookie['name']: cookie['value'] for cookie in super(Browser, self).get_cookies()}

    def get_download_directory(self):
        """Returns path to downloaded file(s) if browser was initiated with capture_download=True"""
        return self.downloader.path

    def downloaded_file(self):
        return self.downloader.open_file()

    def quit(self):
        if not self.running:
            return

        if hasattr(self, 'display'):
            self.display.stop()
        if hasattr(self, 'downloader'):
            self.downloader.clean_up()
        super(Browser, self).quit()
        self.running = False


def with_browser(func, **options):
    """This decorator should be put on a function that uses a Browser to crawl
    something.

    When the function is called, this decorator:

    1. Creates a Browser.
    2. Passes it as an additional argument at the end of the argument list.
    3. Calls the function.
    4. Destroys the browser.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        br = Browser(**options)
        try:
            args = args + (br,)
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            br.quit()
    return wrapper
