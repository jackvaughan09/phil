"""
This is our main data manipulation module
slayer of overflow,
maker of pretty dataframes.
The functions here are run after all dataframes 
have been collected from a file in order
to standardize the output for analysis later on.

Author: @jackvaughan09
"""

import pandas as pd
from config import CANON_HEADERS, AUTOCORRECT_DICT, OVERFLOW_TARGET_COLS 
import code

def polish(df,ref=CANON_HEADERS):
    try:
        df = df.fillna('')
        df = df.applymap(lambda x: str(x).replace('\n',' '))
    except Exception:
        print(f"Error occurred, returning empty df."
               "\nData might have been lost.")
        return pd.DataFrame(columns=ref)
    return df

def standardize_columns(df):  
    for k,v in AUTOCORRECT_DICT.items():
        if k in df.columns:
            df = df.rename(columns={k:v})
    # find difference between df and canon headers
    diff = set(CANON_HEADERS)-set(df.columns) 
    if diff:
        # create the canon column and fill with blank strings
        for label in diff:
            df[label] = ''
    return df

def overflow_repair(df):
    droplist= []
    df = df.fillna('').reset_index(drop=True)
    for i,row in df.iterrows():
        if all([x=='' for x in df.iloc[i]]):
            droplist.append(i)
            continue
        if i == 0:
            continue
        if (
            len(row['audit observation'])== 0 and
            len(row['recommendations'])== 0 and
            len(row['references'])== 0
        ):
            og = df.loc[i-1]
            overflow = df.loc[i]
            comb = [str(og[i])+' '+str(overflow[i]) for i,x in enumerate(og)]
            df.loc[i-1] = comb
            droplist.append(i)

    if droplist == []:
        return df
    for i in droplist:
        df = df.drop(index=i)
    df = df.reset_index(drop=True)
    print(f'Fixed {len(droplist)} overflow rows.')
    return df

def phil_format(dfs,pdf_url):
    print('Applying formatting tools to data...', end=' ')
    dfs = [polish(df) for df in dfs]
    dfs = [standardize_columns(df) for df in dfs]
    dfs = [overflow_repair(df) for df in dfs]
    for df in dfs:
        df['source'] = pdf_url.split('/')[-1]    
    return dfs

#DEPRECATED
# def remove_bad_rows(df):
#     df = df.loc[
#         (df['status of implementation'] != 'Status ofImplementation') &
#         (df['management action'] != 'ManagementAction') &
#         (df['recommendations'] != 'Recommendations')
#     ]
#     df = df.loc[
#         (df['observations and recommendations'] != '')&
#         (df['audit observation'] != '') &
#         (df['recommendations'] != '') &
#         (df['status of implementation'] != '')
#     ]
#     return df