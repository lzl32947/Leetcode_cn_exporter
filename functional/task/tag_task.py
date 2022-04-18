# -*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class TagTask(object):

    @classmethod
    def find_related_div(cls, driver: WebDriver):
        # Find the "相关标签" div
        related_tag = driver.find_element(by=By.CLASS_NAME, value="topic-tags__1S89")
        return related_tag
