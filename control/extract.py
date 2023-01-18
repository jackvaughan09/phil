import tabula.io as tb
import pandas as pd
from extracttools import get_pg_rng, polish, fix_overflow, city, year
from camelot_extract import camelot_extract
from tabula.errors import CSVParseError


def extract(pdf_url) -> pd.DataFrame:
    pg_rng = get_pg_rng(pdf_url)
    if pg_rng == '0':
        return
    try:
        dfs = tb.read_pdf(
            input_path = pdf_url,
            output_format = 'dataframe',
            pages = pg_rng, 
            lattice = True, 
            multiple_tables = True)
    except CSVParseError: #TODO Logging errors
        try:
            return camelot_extract(pdf_url, pg_rng)
        except Exception as e: #TODO: Logging 
            print(e) 
            print(
            'PDF format invalid. Loop will continue, '
            f'but data for {pdf_url} has been lost.')
            return None

    print('Finished reading relevant tables from file')
    dfs = [polish(df) for df in dfs]
    dfs = [dfs[0]]+[fix_overflow(dfs,pg_rng) for df in dfs[1:]] 
    dfs = [year(city(df,pdf_url),pdf_url) for df in dfs]
    print(f'about to concatinate dfs from {pdf_url}')
    out = pd.concat(dfs,ignore_index=True,axis=0)
    return out