'''
Helper functions for camelot_extract.py

Author: @jackvaughan09
'''

import pandas as pd
from extracttools import good_match
from config import CANON_HEADERS

def locate_relevant_camelot_tables(dfs):
    print("Attempting to locate relevant tables...")
    out = []  
    counter = 0                          
    for i, df in enumerate(dfs):
        # camelot shoves the column headers into the first row of the df
        # clean and store values
        columns = df.iloc[0].apply(lambda x: x.replace('\n',''))
        columns = [good_match(col,CANON_HEADERS) for col in columns]
        # fuzzy logic check if column names match target headers
        # if no, remove df from dfs
        try:
            if len(set(CANON_HEADERS).intersection(set(columns))) <= 2:
                counter += 1
                continue
        except Exception as e:
            print(f"Error: {e}")
        if len(out)<1:
            print('No relevant tables found.')
            return pd.DataFrame(columns=CANON_HEADERS)
        # if yes, then make the first row the headers of the new df
        df.columns = columns
        df = df.iloc[1:] 
        out.append(df.astype(str))


    print(f'Collected {len(out)} tables!\n'
          f'Removed {counter}')
    return out

    


