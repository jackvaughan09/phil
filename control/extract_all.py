import extract
import os
import pandas as pd
def extract_all(pdf_dir) -> pd.DataFrame:
    df = pd.DataFrame()
    for file in os.listdir(pdf_dir):
        df.append(extract(file))
    return df
