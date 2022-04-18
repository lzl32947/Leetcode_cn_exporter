# -*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class LoginTask(object):

    @classmethod
    def find_login_with_user_passwd_button(cls, driver: WebDriver):
        # Find the "帐号密码登录" button
        switch_button = driver.find_element(by=By.CLASS_NAME, value="e19orumq1")
        return switch_button

    @classmethod
    def find_login_user(cls, driver: WebDriver):
        # Find the inputText "手机/邮箱"
        login_input = driver.find_element(by=By.NAME, value="login")
        return login_input

    @classmethod
    def find_login_passwd(cls, driver: WebDriver):
        # Find the inputText "输入密码"
        login_passwd = driver.find_element(by=By.NAME, value="password")
        return login_passwd

    @classmethod
    def find_login_click_button(cls, driver: WebDriver):
        # Find the "登陆" button
        button = driver.find_element(by=By.CLASS_NAME, value="e4jw0mn0")
        return button
