# -*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CounterTask(object):
    @classmethod
    def find_problem_list_bottom(cls, driver: WebDriver):
        # Find the "题目列表" button on bottom left
        switch_button = driver.find_element(by=By.XPATH, value="(//div[@class='question-fast-picker__3qGP']//button)[1]")
        return switch_button

    @classmethod
    def find_filter_button(cls, driver: WebDriver):
        # Find the "(筛选)" button
        filter_button = driver.find_element(by=By.XPATH, value="//button[contains(@class,'false css-qq9uua-night-sm-Btn')]")
        return filter_button

    @classmethod
    def find_next_page_button(cls, driver: WebDriver):
        # Find the "(下一页)" button
        filter_button = driver.find_element(by=By.XPATH, value="(//button[@class='css-qq9uua-night-sm-Btn e131m59q0'])[2]")
        return filter_button

    @classmethod
    def find_previous_page_button(cls, driver: WebDriver):
        # Find the "(上一页)" button
        filter_button = driver.find_element(by=By.XPATH, value="(//button[@class='css-qq9uua-night-sm-Btn e131m59q0'])[1]")
        return filter_button

    @classmethod
    def find_easy_button(cls, driver: WebDriver):
        # Find the "简单(难度)" button
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='EASY']")
        return buttons

    @classmethod
    def find_medium_button(cls, driver: WebDriver):
        # Find the "中等(难度)" button
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='MEDIUM']")
        return buttons

    @classmethod
    def find_hard_button(cls, driver: WebDriver):
        # Find the "困难(难度)" button
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='HARD']")
        return buttons

    @classmethod
    def find_todo_button(cls, driver: WebDriver):
        # Find the "未做(状态)" button
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='TODO']")
        return buttons

    @classmethod
    def find_solved_button(cls, driver: WebDriver):
        # Find the "已解答(状态)" button
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='SOLVED']")
        return buttons

    @classmethod
    def find_attempted_button(cls, driver: WebDriver):
        # Find the "尝试过(状态)" button
        buttons = driver.find_element(by=By.XPATH, value="//div[@data-value='ATTEMPTED']")
        return buttons

    @classmethod
    def find_all_page_problems(cls, driver: WebDriver):
        # Find the area of document
        raw_document = driver.find_element(by=By.CLASS_NAME, value="question-list__1Kev")
        return raw_document
