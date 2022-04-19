from config.globals import global_browser
from config.options import WebOptions
from config.url import MAIN_PAGE_URL
from functional.parse.parse_counter import parse_counter
from functional.process.count_solved_process import CountSolvedProcess
from util.drivers import Driver


def output_problem_to_sqls(cookies_store):
    Driver().init(global_browser, WebOptions().get_option(global_browser), renew=True)
    Driver().set_cookies(cookies_store, MAIN_PAGE_URL)
    result = CountSolvedProcess().run()
    Driver().close_single()
    if result[0]:
        parse_result = parse_counter(result[1])
        return parse_result
    else:
        return None
