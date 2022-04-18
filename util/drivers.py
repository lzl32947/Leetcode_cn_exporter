import threading
from typing import Any, List, Dict, Optional

import selenium.common.exceptions
from selenium.webdriver import *
from selenium.webdriver.remote.webdriver import WebDriver

from config.enums import Browser


class Driver(object):
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        if not hasattr(self, "driver_arr"):
            self.driver_arr: List[Optional[WebDriver]] = [None] * 10

    def __new__(cls, *args, **kwargs):
        if not hasattr(Driver, "_instance"):
            with Driver._instance_lock:
                if not hasattr(Driver, "_instance"):
                    Driver._instance = object.__new__(cls)
        return Driver._instance

    def get_driver(self, order: int = 0) -> WebDriver:
        """
        Get the webdriver if already had one
        :except RuntimeError, if the webdriver had not been initialized
        :return: Webdriver instance
        """
        if self.driver_arr[order]:
            return self.driver_arr[order]
        else:
            raise RuntimeError("The Webdriver has not been initialized!")

    def set_cookies(self, cookies: List[Dict], url: str, order: int = 0) -> None:
        """
        Set the cookies for the driver instance
        :param cookies: List[Dict], the cookies
        :param url: str, the target url
        :except RuntimeError, if the webdriver had not been initialized
        :return: None
        """
        if self.driver_arr[order]:
            self.driver_arr[order].get(url)
            for item in cookies:
                self.driver_arr[order].add_cookie(item)
            self.driver_arr[order].refresh()
        else:
            raise RuntimeError("The Webdriver has not been initialized!")

    def init(self, driver_type: Optional[Browser], driver_option: Any, order: int = 0, renew: bool = False) -> None:
        """
        Init the webdriver
        :param driver_type: Browser, the driver type, Edge driver by default
        :param driver_option: Any, the options for the web driver
        :return: None
        """
        if self.driver_arr[order] is not None:
            if renew:
                self.close_single(order)
            else:
                pass
        else:
            if driver_type == Browser.EDGE:
                self.driver_arr[order] = Edge(options=driver_option)
            else:
                self.driver_arr[order] = Edge(options=driver_option)

    def close_single(self, order: int = 0) -> bool:
        """
        Close the driver
        :except selenium Error, if can't close
        :return: bool, whether close successfully
        """
        if self.driver_arr[order]:
            try:
                self.driver_arr[order].quit()
                self.driver_arr[order] = None
                return True
            except selenium.common.exceptions.WebDriverException:
                return False
        else:
            return True

    def close_all(self) -> bool:
        flag = True
        for i in range(len(self.driver_arr)):
            flag = flag and self.close_single(i)
        return flag
