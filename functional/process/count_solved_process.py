import time
from time import sleep
from typing import Tuple, Any

from selenium.webdriver.support.wait import WebDriverWait

from config.url import PROBLEM_EXAMPLE_URL
from functional.process.base_process import BaseProcess
from functional.task.count_task import CounterTask


class CountSolvedProcess(BaseProcess):
    """
    The COUNTER process
    :aims: To counter all the solved problems
    """

    def run(self) -> Tuple[bool, Any]:
        # Get the problem url
        self.driver.get(PROBLEM_EXAMPLE_URL)

        WebDriverWait(self.driver, 2).until(lambda d: CounterTask.find_problem_list_bottom(d))
        time.sleep(0.5)
        CounterTask.find_problem_list_bottom(self.driver).click()

        WebDriverWait(self.driver, 2).until(lambda d: CounterTask.find_filter_button(d))
        time.sleep(0.5)
        CounterTask.find_filter_button(self.driver).click()

        WebDriverWait(self.driver, 2).until(lambda d: CounterTask.find_solved_button(d))
        time.sleep(0.5)
        CounterTask.find_solved_button(self.driver).click()

        prev_document = None
        documents = []
        count = 1
        while True:
            sleep(1)
            document = CounterTask.find_all_page_problems(self.driver)

            if document.text == prev_document:
                # The end of the document
                return True, documents
            else:
                # Update until the end
                prev_document = document.text
                documents.append(document.get_attribute("outerHTML"))
                count += 1
            CounterTask.find_next_page_button(self.driver).click()

        return False, []
