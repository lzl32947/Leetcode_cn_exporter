from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.options import ArgOptions

from config.enums import Browser


class Options(object):
    """
    Custom the driver options
    """

    def __init__(self):
        self.edge_option = EdgeOptions()
        # The followings two are necessary!
        self.edge_option.add_argument("--disable-blink-features")
        self.edge_option.add_argument("--disable-blink-features=AutomationControlled")

    def get_option(self, browser: Browser) -> ArgOptions:
        """
        Get the options
        :param browser: enums.Browser, browser type
        :return: selenium.webdriver.common.options.ArgOptions, the options for browsers
        """
        if browser == Browser.EDGE:
            return self.edge_option
