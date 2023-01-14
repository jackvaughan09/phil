import tabula.io as tb
import pandas as pd
from extracttools import get_pg_rng, polish, overflow_check
from config import CANON_HEADERS
def extract(pdf_url) -> pd.DataFrame:
    pg_rng = get_pg_rng(pdf_url)
    dfs = tb.read_pdf(input_path = pdf_url, output_format = 'dataframe', pages = pg_rng, lattice = True, multiple_tables = True)
    dfs = [polish(df) for df in dfs]
    dfs = [overflow_check(df,CANON_HEADERS,dfs[0]) for df in dfs[1:]]
    out = pd.DataFrame()
    for df in dfs:
        out.append(df,ignore_index=True)
        print(df)
    return out