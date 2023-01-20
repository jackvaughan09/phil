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
        print('Cleaning headers...', end=' ')
        # camelot shoves the column headers into the first row of the df
        # clean and store values
        columns = df.iloc[0].apply(lambda x: x.replace('\n',''))
        columns = [good_match(col,CANON_HEADERS) for col in columns]
        print('Done!')
        # fuzzy logic check if column names match target headers
        # if no, remove df from dfs
        print('Checking for relevance...', end=' ')
        try:
            if len(set(CANON_HEADERS).intersection(set(columns))) <= 2:
                counter += 1
                print(f'Irrelevant, removed table {i+1}/{len(dfs)}')
                continue
        except Exception as e:
            print(f"Error: {e}")
        
        print('Relevant table collected!')
        # if yes, then make the first row the headers of the new df
        df.columns = columns
        df = df.iloc[1:] 
        out.append(df.astype(str))
    if len(out)<1:
        print('No relevant tables found.')
        return pd.DataFrame(columns=CANON_HEADERS)

    print(f'Collected {len(out)} tables!\n'
          f'Removed {counter}')
    return out

def camelot_polish(df,ref):
    #replacing \n throughout
    try:
        df = df.replace(r'\n',' ',regex=True)
    except TypeError:
        print(f"Nothing to polish! Returning empty df.")
        return pd.DataFrame(columns=ref)
    return df
    


