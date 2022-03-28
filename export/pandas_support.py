import os.path
from typing import List, Tuple, Union, Optional, Dict

import pandas as pd


def export_to_pandas(document: Union[List, Dict], head: Optional[Union[Tuple, List]]):
    df = None
    if isinstance(document, list):
        df = pd.DataFrame(document, columns=head)
    return df


def export_to_excel(file_name: str, document: Union[List, Dict], head: Optional[Union[Tuple, List]]):
    if not file_name.endswith(".xlsx"):
        file_name = file_name + ".xlsx"
    df = export_to_pandas(document, head)
    df.to_excel(os.path.join("output", file_name))


def export_to_csv(file_name: str, document: Union[List, Dict], head: Optional[Union[Tuple, List]]):
    if not file_name.endswith(".csv"):
        file_name = file_name + ".csv"
    df = export_to_pandas(document, head)
    df.to_csv(os.path.join("output", file_name))
