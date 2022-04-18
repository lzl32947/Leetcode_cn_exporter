import time

from selenium.webdriver.support.wait import WebDriverWait

from config.url import PROBLEM_URL
from functional.process.base_process import BaseProcess
from functional.task.tag_task import TagTask


class TagProcess(BaseProcess):

    def run(self, *args, **kwargs):
        self.driver.get(PROBLEM_URL + args[0])

        WebDriverWait(self.driver, 2).until(lambda d: TagTask.find_related_div(d))
        time.sleep(0.5)

        tag = TagTask.find_related_div(self.driver).get_attribute("outerHTML")
        return tag
