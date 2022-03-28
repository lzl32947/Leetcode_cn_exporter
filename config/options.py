from selenium.webdriver import EdgeOptions

from config.enums import Browser


class Options(object):
    def __init__(self):
        self.edge_option = EdgeOptions()
        self.edge_option.add_argument("--disable-blink-features")
        self.edge_option.add_argument("--disable-blink-features=AutomationControlled")

    def get_option(self, browser: Browser):
        if browser == Browser.EDGE:
            return self.edge_option
