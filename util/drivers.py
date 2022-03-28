import threading
from typing import Any

from selenium.webdriver import *

from config.enums import Browser


class Driver(object):
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        if not hasattr(self, "driver"):
            self.driver = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(Driver, "_instance"):
            with Driver._instance_lock:
                if not hasattr(Driver, "_instance"):
                    Driver._instance = object.__new__(cls)
        return Driver._instance

    def get_driver(self):
        if self.driver:
            return self.driver
        else:
            raise RuntimeError()

    def init(self, driver_type: Browser, driver_option: Any):
        if driver_type == Browser.EDGE:
            self.driver = Edge(options=driver_option)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
