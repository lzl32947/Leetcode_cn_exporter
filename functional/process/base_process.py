from abc import abstractmethod
from typing import Tuple

from selenium.webdriver import Edge

from util.drivers import Driver


class BaseProcess():

    def __init__(self):
        self.driver: Edge = Driver().get_driver()

    @abstractmethod
    def run(self, *args, **kwargs) -> Tuple[bool, ...]:
        pass
