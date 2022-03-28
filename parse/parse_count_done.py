from typing import List

import bs4


def parse_count_done(documents: List[str]):
    general_output = []
    for index, content in enumerate(documents):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        questions = soup.select(".question__3lUu")
        for item in questions:
            difficult = item.select(".eaz8kc70")[0].text
            name = item.select("span")[1].text
            ids = item.get("data-question-id")
            english_title = item.get("title")
            general_output.append((ids, english_title, name, difficult))
    return general_output
