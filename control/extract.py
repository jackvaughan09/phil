"""
Author: @jackvaughan09
"""

import camelot
import pandas as pd
from config import CANON_HEADERS
from extracttools import locate_relevant_tables, get_pg_rng
from philformat import overflow_repair, phil_format


def extract(pdf_url):
    pg_rng = get_pg_rng(pdf_url)
    if len(pg_rng) == 0:
        print("No tables found. Continuing.")
        return pd.DataFrame(columns=CANON_HEADERS)

    print(f"Attempting to read tables from: {pdf_url}" "\nThis might take a while.")
    dfs = [
        df.df.astype(str)
        for df in camelot.read_pdf(
            filepath=pdf_url,
            flavor="lattice",
            multiple_tables=True,
            copy_text=["v"],
            line_scale=30,
            pages=get_pg_rng(pdf_url),
        )
    ]
    if len(dfs) < 1:
        print("No tables found. Continuing.")
        return pd.DataFrame(columns=CANON_HEADERS)
    print(f"Finished reading {len(dfs)} tables from file {pdf_url}")
    dfs = locate_relevant_tables(dfs)
    if type(dfs) == pd.DataFrame:
        return dfs

    dfs = phil_format(dfs, pdf_url)
    out = pd.concat(dfs).reset_index(drop=True)
    # one more for good measure.
    out = overflow_repair(out)
    return out
