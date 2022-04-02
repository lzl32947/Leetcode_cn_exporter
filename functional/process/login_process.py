import time
from typing import Tuple

from selenium.webdriver.support.wait import WebDriverWait

from config.url import LOGIN_URL
from functional.process.base_process import BaseProcess
from functional.task.login_task import LoginTask


class LoginProcess(BaseProcess):

    def run(self, *args, **kwargs) -> Tuple[bool, ...]:
        try:
            user = kwargs["user"]
            passwd = kwargs["passwd"]
        except KeyError as e:
            return False,
        self.driver.get(LOGIN_URL)
        WebDriverWait(self.driver, 2).until(lambda d: LoginTask.find_login_click_button(d))
        LoginTask.find_login_with_user_passwd_button(self.driver).click()

        LoginTask.find_login_user(self.driver).send_keys(user)
        LoginTask.find_login_passwd(self.driver).send_keys(passwd)
        LoginTask.find_login_click_button(self.driver).click()

        time.sleep(5)
        if self.driver.current_url != LOGIN_URL:
            return True,
        else:
            return False,
