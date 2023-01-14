from extract import extract
import os
import pandas as pd
from config import CANON_HEADERS
def extract_all(pdf_dir) -> pd.DataFrame:
    df = pd.DataFrame(columns=CANON_HEADERS)
    for fi in os.listdir(pdf_dir):
        if os.path.splitext(fi)[1] == '.pdf':
            df = pd.concat([df,extract(os.path.join(pdf_dir,fi))], ignore_index = True)
    return df
