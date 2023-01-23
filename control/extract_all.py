import os
import pandas as pd
from camelot_extract import camelot_extract


def extract_all(pdf_dir) -> pd.DataFrame:
    dfs = []
    print('Beginning extraction process...')
    for fi in os.listdir(pdf_dir):
        if os.path.splitext(fi)[1] == '.pdf':
            dfs.append(camelot_extract(os.path.join(pdf_dir,fi)))
    print('Finished extracting relevant tables from all files')
    
    print('Time to do some cleaning!')
    # remove NoneType dfs (there shouldn't be any but this is safe.)
    dfs = list(filter(lambda x: x is not None,dfs))
    print('Nonetype values removed.')
    # concat result
    full_df = pd.concat(dfs)
    #full_df = remove_bad_rows(full_df).reset_index(drop=True)
    return full_df
