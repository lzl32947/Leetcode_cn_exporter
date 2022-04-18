from typing import Tuple, List

import bs4


def parse_tag(documents: str) -> List[Tuple[str, str]]:
    """
    Parse the document
    :param documents:
    :return:
    """
    ans = []
    soup = bs4.BeautifulSoup(documents, 'html.parser')
    for i in soup.select("a"):
        tag_link = i.get("href").split("/")[-1]
        if tag_link == "":
            tag_link = i.get("href").split("/")[-2]
        tag_text = i.text
        ans.append((tag_link, tag_text))
    return ans
