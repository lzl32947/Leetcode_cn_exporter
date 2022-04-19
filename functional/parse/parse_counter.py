import re
from typing import List

import bs4


def parse_counter(documents: List[str]):
    """
    Parse the document
    :param documents:
    :return:
    """
    general_output = []
    for index, content in enumerate(documents):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        questions = soup.select(".question__3lUu")
        for item in questions:
            difficulty = item.select(".eaz8kc70")[0].text
            full_title = item.select("span")[1].text
            problem_id = item.get("data-question-id")
            link = item.get("title")
            rx = re.compile(r"#(\d+\s|LCS\s\d+\s|面试题\s.*?\s|剑指 Offer\s.*?\d+-\s.*?\s|剑指 Offer\s\d+\s-\s.*?\s|剑指 Offer\s.*?\d+\s)")
            try:
                result = rx.match(full_title)
                result = result.group(0)
            except AttributeError:
                print(full_title)
            identifier = result[1:-1]
            title = full_title[len(identifier) + 2:]
            general_output.append((problem_id, identifier, title, full_title, link, difficulty))
    return general_output
