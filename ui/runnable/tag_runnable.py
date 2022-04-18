import sqlite3
from typing import List, Dict

from config.globals import global_browser
from config.options import WebOptions
from config.url import MAIN_PAGE_URL
from functional.parse.parse_tag import parse_tag
from functional.process.tag_process import TagProcess
from util.drivers import Driver
from util.sql import SQLiteDriver


def list_tags(cookies_store: List[Dict], problem_set: List[tuple]):
    Driver().init(global_browser, WebOptions().get_option(global_browser), renew=True)
    Driver().set_cookies(cookies_store, MAIN_PAGE_URL)
    SQLiteDriver().create_conn("general")
    for problem_id, problem_link in problem_set:
        result = TagProcess().run(problem_link)
        if result[0]:
            try:
                parse_result = parse_tag(result[1])
                for link, text in parse_result:
                    if not SQLiteDriver().find_exist("general", "TAGS", "tag_name", "=\"{}\"".format(text)):
                        SQLiteDriver().insert_into_tags("general", [(text, link)])
                    tag_id = SQLiteDriver().find_tag_id("general", tag_name=text)
                    if tag_id:
                        SQLiteDriver().insert_into_problems_tags("general", [(problem_id, tag_id)])
            except sqlite3.Error as e:
                print(e)
        else:
            print(problem_id, problem_link)

    Driver().close_single()


if __name__ == '__main__':
    list_tags(None, None)
