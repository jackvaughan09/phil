import pandas as pd
from extracttools import good_match
from config import CANON_HEADERS
import camelot
import code

def locate_relevant_camelot_tables(dfs):
    print("Attempting to locate relevant tables...")
    out = []  
    counter = 0                          
    for i, df in enumerate(dfs):
        print('Cleaning headers...', end=' ')
        # camelot shoves the column headers into the first row of the df
        # clean and store values
        df.iloc[0]= df.iloc[0].apply(lambda x: x.replace('\n',''))
        columns = df.iloc[0]
        columns = [good_match(col,CANON_HEADERS) for col in columns]
        print('Done!')
        # fuzzy logic check if first row is good match of target headers
        # if no, remove df from dfs
        print('Checking for relevance...', end=' ')
        try:
            if len(set(CANON_HEADERS).intersection(set(columns))) <= 4:
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
        return pd.DataFrame(columns=CANON_HEADERS)

    print(f'Collected {len(out)} tables!\n'
          f'Removed {counter}')
    return out

def camelot_polish(df):
    return df.replace(r'\n','',regex=True)

def camelot_overflow_repair(df):
    overflow_rows = [i for i,x in enumerate(df['']) if x == '']
    for i in overflow_rows:
        df.loc[i-1]+=df.loc[i]
    df = df.drop(index=overflow_rows).reset_index(drop=True)
    return df

def camelot_extract(pdf_url, pg_rng):
    print('Attempting alternate file reader,'
          '\nThis might take a while.')     # <-- valid syntax
    
    # ensure string typing, keeps code from breaking later on
    dfs = [df.df.astype(str) for df in camelot.read_pdf(
        filepath = pdf_url,
        pages = pg_rng,                 #TODO: improving pg_rng function accuracy:
        flavor = 'lattice',
        multiple_tables = True,                   
    )]                                  
    print('Finished reading all tables from file')
    dfs = locate_relevant_camelot_tables(dfs)
    dfs = [camelot_polish(df) for df in dfs]
    out = pd.concat(dfs,ignore_index=True,axis=0)
    out = camelot_overflow_repair(out)
    return out


