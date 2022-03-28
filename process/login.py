import time
from typing import Tuple

from selenium.webdriver.support.wait import WebDriverWait

from config.PASSWD import USER, PASSWD
from config.url import LOGIN_URL
from process.base_process import BaseProcess
from task.login import LoginTask


class LoginProcess(BaseProcess):

    def run(self) -> Tuple[bool, ...]:
        self.driver.get(LOGIN_URL)
        WebDriverWait(self.driver, 2).until(lambda d: LoginTask.find_login_click_button(d))
        LoginTask.find_login_with_user_passwd_button(self.driver).click()

        LoginTask.find_login_user(self.driver).send_keys(USER)
        LoginTask.find_login_passwd(self.driver).send_keys(PASSWD)
        LoginTask.find_login_click_button(self.driver).click()

        time.sleep(5)
        if self.driver.current_url != LOGIN_URL:
            return True,
        else:
            return False,
