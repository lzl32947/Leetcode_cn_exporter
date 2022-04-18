from config.globals import global_browser
from config.options import WebOptions
from functional.process.login_process import LoginProcess
from util.drivers import Driver


def login_via_browser(user: str, passwd: str):
    Driver().init(global_browser, WebOptions().get_option(global_browser), renew=True)
    result = LoginProcess().run(user=user, passwd=passwd)
    Driver().close_single()
    if result[0]:
        return result[1]
    else:
        return None
