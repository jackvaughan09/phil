import tabula.io as tb
import pandas as pd
from extracttools import get_pg_rng, polish, fix_overflow, city, year
from config import CANON_HEADERS
def extract(pdf_url) -> pd.DataFrame:
    pg_rng = get_pg_rng(pdf_url)
    if pg_rng == '0':
        return
    print(pg_rng)
    dfs = tb.read_pdf(input_path = pdf_url, output_format = 'dataframe', pages = pg_rng, lattice = True, multiple_tables = True)
    dfs = [polish(df) for df in dfs]
    dfs = [dfs[0]]+[fix_overflow(dfs,pg_rng) for df in dfs[1:]]
    dfs = [year(city(df,pdf_url),pdf_url) for df in dfs]
    out = pd.concat(dfs,ignore_index=True,axis=0)
    return out