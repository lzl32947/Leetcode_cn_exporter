from config.enums import Browser
from config.options import Options
from export.pandas_support import export_to_excel
from parse.parse_count_done import parse_count_done
from process.count_process import CountProcess
from process.login import LoginProcess
from util.drivers import Driver

try:
    Driver().init(Browser.EDGE, Options().get_option(Browser.EDGE))
    if LoginProcess().run()[0]:
        flag, doc = CountProcess().run()
        parse_result = parse_count_done(doc)
        export_to_excel("done", parse_result, head=("ID", "Title", "题目名", "困难度"))
    Driver().close()
except Exception as e:
    Driver().close()
    raise e
