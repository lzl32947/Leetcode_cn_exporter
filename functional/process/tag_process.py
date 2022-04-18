import time

import selenium.common.exceptions
from selenium.webdriver.support.wait import WebDriverWait

from config.url import PROBLEM_URL
from functional.process.base_process import BaseProcess
from functional.task.tag_task import TagTask


class TagProcess(BaseProcess):

    def run(self, *args, **kwargs):
        try:
            self.driver.get(PROBLEM_URL + args[0])

            WebDriverWait(self.driver, 2).until(lambda d: TagTask.find_related_div(d))
            time.sleep(5)

            tag = TagTask.find_related_div(self.driver).get_attribute("outerHTML")
            time.sleep(1)
            return True, tag
        except selenium.common.exceptions.WebDriverException as e:
            print(e)
            return False, None
