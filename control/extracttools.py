"""
Helper functions for extract.py

Author: @jackvaughan09 + @hudnash
"""

import pandas as pd
import PyPDF2 as p
from config import CANON_HEADERS, TARGET_SENTENCE
from fuzzywuzzy import fuzz


def get_pg_rng(pdf_url):
    out = []
    reader = p.PdfReader(pdf_url)
    pg_count = len(reader.pages)
    if pg_count > 100:  # arbitrarily chosen
        for i, pg in enumerate(reader.pages):
            content = pg.extract_text()
            if len(
                [target for target in TARGET_SENTENCE if target in content.lower()]
            ) == len(TARGET_SENTENCE):
                out.append(str(i))
                # camelot starts at page 1 but here it's 0 indexed
        if len(out) == 0:
            return "0"
        return ",".join(out) + "-end"
    else:
        return "1-end"


def good_match(og: str, ref: list[str]):
    good = ""
    approx = 0
    og = og.lower()
    for target in ref:
        new_approx = fuzz.token_sort_ratio(og, target)
        if new_approx > approx:
            approx = new_approx
            good = target
    if approx < 60:
        good = og
    return good


def locate_relevant_tables(dfs):
    print("Attempting to locate relevant tables...")
    out = []
    removal_counter = 0
    for i, df in enumerate(dfs):
        # camelot shoves the column headers into the first row of the df
        # clean and store values
        columns = df.iloc[0].apply(lambda x: x.replace("\n", ""))
        columns = [good_match(col, CANON_HEADERS) for col in columns]
        # fuzzy logic check if column names match target headers
        # if no, remove df from dfs
        try:
            if len(set(CANON_HEADERS).intersection(set(columns))) <= 2:
                removal_counter += 1
                continue
        except Exception as e:
            print(f"Error: {e}")

        # if yes, then make the first row the headers of the new df
        df.columns = columns
        df = df.iloc[1:]
        out.append(df.astype(str))

    if len(out) < 1:
        print("No relevant tables found.")
        return pd.DataFrame(columns=CANON_HEADERS)

    print(f"Collected {len(out)} tables!\n" f"Removed {removal_counter}")
    return out
