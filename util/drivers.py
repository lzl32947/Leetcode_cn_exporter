import threading
from typing import Any, List, Dict

from selenium.webdriver import *
from selenium.webdriver.remote.webdriver import WebDriver

from config.enums import Browser


class Driver(object):
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        if not hasattr(self, "driver"):
            self.driver: WebDriver = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(Driver, "_instance"):
            with Driver._instance_lock:
                if not hasattr(Driver, "_instance"):
                    Driver._instance = object.__new__(cls)
        return Driver._instance

    def get_driver(self) -> WebDriver:
        if self.driver:
            return self.driver
        else:
            raise RuntimeError()

    def set_cookies(self, cookies: List[Dict], url: str):
        if self.driver:
            self.driver.get(url)
            for item in cookies:
                self.driver.add_cookie(item)
            self.driver.refresh()

    def init(self, driver_type: Browser, driver_option: Any):
        if driver_type == Browser.EDGE:
            self.driver = Edge(options=driver_option)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
