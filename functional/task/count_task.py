from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CountDoneTask(object):
    @classmethod
    def find_problem_list_bottom(cls, driver: WebDriver):
        switch_button = driver.find_element(by=By.XPATH, value="(//div[@class='question-fast-picker__3qGP']//button)[1]")
        return switch_button

    @classmethod
    def find_filter_button(cls, driver: WebDriver):
        filter_button = driver.find_element(by=By.XPATH, value="//button[contains(@class,'false css-qq9uua-night-sm-Btn')]")
        return filter_button

    @classmethod
    def find_next_page_button(cls, driver: WebDriver):
        filter_button = driver.find_element(by=By.XPATH, value="(//button[@class='css-qq9uua-night-sm-Btn e131m59q0'])[2]")
        return filter_button

    @classmethod
    def find_previous_page_button(cls, driver: WebDriver):
        filter_button = driver.find_element(by=By.XPATH, value="(//button[@class='css-qq9uua-night-sm-Btn e131m59q0'])[1]")
        return filter_button

    @classmethod
    def find_easy_button(cls, driver: WebDriver):
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='EASY']")
        return buttons

    @classmethod
    def find_medium_button(cls, driver: WebDriver):
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='MEDIUM']")
        return buttons

    @classmethod
    def find_hard_button(cls, driver: WebDriver):
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='HARD']")
        return buttons

    @classmethod
    def find_todo_button(cls, driver: WebDriver):
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='TODO']")
        return buttons

    @classmethod
    def find_solved_button(cls, driver: WebDriver):
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='SOLVED']")
        return buttons

    @classmethod
    def find_attempted_button(cls, driver: WebDriver):
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='ATTEMPTED']")
        return buttons

    @classmethod
    def find_all_page_problems(cls, driver: WebDriver):
        raw_document = driver.find_element(by=By.CLASS_NAME, value="question-list__1Kev")
        return raw_document
