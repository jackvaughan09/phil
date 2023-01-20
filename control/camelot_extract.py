'''
This file presents an alternate PDF Reader Library -- Camelot
as an optimal solution for scraping PDFs of non-specific
file formats (those that do not match Adobe's standards)

Author: @jackvaughan09
'''

import pandas as pd
from extracttools import get_pg_rng, year, city
from camelot_tools import locate_relevant_camelot_tables
from philformat import phil_format, overflow_repair
from config import CANON_HEADERS
import camelot
import code

def camelot_extract(pdf_url):
    pg_rng = get_pg_rng(pdf_url) #TODO: improving pg_rng function accuracy:
    if pg_rng == '0':
        return
    print(f'Attempting to read tables from: {pdf_url}'
          '\nThis might take a while.')    
    
    # ensure string typing
    dfs = [df.df.astype(str) for df in camelot.read_pdf(
        filepath = pdf_url,                
        flavor = 'lattice',
        multiple_tables = True,
        copy_text = ['v'], 
        line_scale = 30,
        pages = pg_rng
    )]                                  
    if len(dfs)< 1:
        print('No tables found. Continuing.')
        return pd.DataFrame(columns=CANON_HEADERS)
    print(f'Finished reading {len(dfs)} tables from file {pdf_url}')
    dfs = locate_relevant_camelot_tables(dfs)
    dfs = phil_format(dfs, pdf_url)
    out = pd.concat(dfs).reset_index(drop=True)
    out = overflow_repair(out)
    return out


