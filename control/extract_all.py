from extract import extract
import os
import pandas as pd
from config import CANON_HEADERS, AUTOCORRECT_DICT


def assert_canon_columns(dfs):
    for i, df in enumerate(dfs):
        # Implement autocorrect for column names
        for k,v in AUTOCORRECT_DICT.items():
            if k in df.columns:
                dfs[i] = dfs[i].rename(columns={k:v})
        # find difference between df and canon headers
        diff = set(CANON_HEADERS)-set(df.columns) 
        if diff:
            # create the canon column and fill with blank strings
            for label in diff:
                dfs[i][label] = ''
    return dfs

def remove_body_header_rows(df):
    df = df.loc[
        (df['status of implementation'] != 'Status ofImplementation') &
        (df['management action'] != 'ManagementAction') &
        (df['recommendations'] != 'Recommendations')
    ]
    return df

def extract_all(pdf_dir) -> pd.DataFrame:
    dfs = []
    for fi in os.listdir(pdf_dir):
        if os.path.splitext(fi)[1] == '.pdf':
            dfs.append(extract(os.path.join(pdf_dir,fi)))
    # remove NoneType values
    dfs = list(filter(lambda x: x is not None,dfs))
    # then assert equal columns
    dfs = assert_canon_columns(dfs)
    # concat result
    full_df = pd.concat(dfs)
    full_df = remove_body_header_rows(full_df)
    return full_df
