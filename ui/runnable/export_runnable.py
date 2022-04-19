import os.path
import time

import pandas as pd
from pandas import DataFrame

from util.sql import SQLiteDriver


def export_from_sql_to_xlsx(database_name: str):
    problems_list = SQLiteDriver().find_all_problems_with_tags(database_name)
    tag_problems_dict = SQLiteDriver().find_all_problem_by_tags(database_name)
    problems_dataframe = DataFrame(problems_list, columns=["problem_id", "identifier", "title", "full_title", "link", "difficulty", "tags"])
    problems_dataframe.sort_values(by=['problem_id'], inplace=True)
    tag_dataframe = {}
    for key in tag_problems_dict:
        sub_problem_dataframe = DataFrame(tag_problems_dict[key], columns=["problem_id", "identifier", "title", "full_title", "link", "difficulty"])
        sub_problem_dataframe.sort_values(by=['problem_id'], inplace=True)
        tag_dataframe[key] = sub_problem_dataframe
    now_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    writer = pd.ExcelWriter(os.path.join("output", "{}.xlsx".format(now_time)))
    problems_dataframe.to_excel(writer, database_name, index=False, encoding="utf-8")
    for tag in tag_dataframe:
        tag_dataframe[tag].to_excel(writer, tag, index=False, encoding="utf-8")
    writer.save()
    writer.close()
