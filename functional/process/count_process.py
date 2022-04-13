from time import sleep
from typing import Tuple, Any

from selenium.webdriver.support.wait import WebDriverWait

from config.url import PROBLEM_EXAMPLE_URL
from functional.process.base_process import BaseProcess
from functional.task.count_task import CountDoneTask


class CountProcess(BaseProcess):

    def run(self) -> Tuple[bool, Any]:
        self.driver.get(PROBLEM_EXAMPLE_URL)
        WebDriverWait(self.driver, 2).until(lambda d: CountDoneTask.find_problem_list_bottom(d))
        CountDoneTask.find_problem_list_bottom(self.driver).click()

        WebDriverWait(self.driver, 2).until(lambda d: CountDoneTask.find_filter_button(d))
        CountDoneTask.find_filter_button(self.driver).click()

        WebDriverWait(self.driver, 2).until(lambda d: CountDoneTask.find_solved_button(d))
        CountDoneTask.find_solved_button(self.driver).click()

        prev_document = None
        documents = []
        count = 1
        while True:
            sleep(1)
            document = CountDoneTask.find_all_page_problems(self.driver)

            if document.text == prev_document:
                return True, documents
            else:
                prev_document = document.text
                documents.append(document.get_attribute("outerHTML"))
                count += 1
            CountDoneTask.find_next_page_button(self.driver).click()

        return False, []
