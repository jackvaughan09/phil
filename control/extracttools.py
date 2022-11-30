import tabula.io as tab
import pandas as pd
from difflib import SequenceMatcher
import PyPDF2 as p
import os
def default(filename):
    dfs = tab.read_pdf(filename,lattice=True,pages='all') # pages attribute of tabula-py is broken
    return dfs
def rename_columns(dfs:list) -> pd.DataFrame:
    cols = [df.columns for df in dfs]
    print(cols)
def add_filename_col(fn,df):
    df['filename']=[fn for row in range(len(df))]
    return df[['filename']+[col for col in df if col not in ['filename']]]
def delete_pages_before(filename,start_page):
    infile = p.PdfReader(filename, 'rb')
    pages_to_keep = range(start_page, infile.numPages) # page numbering starts from 0
    output = p.PdfWriter()
    for i in pages_to_keep:
        page = infile.pages[i] 
        output.add_page(page)
        with open(filename, 'wb') as f:
            output.write(f)
from fuzzywuzzy import fuzz
import config as conf
def add_date_cols(df,fn): # add file download date from metadata and other dates from metadata and date or year published
    pass # TODO: 11/30/22
def add_location_col(df,fn): # add location from filename
    pass # TODO: 11/30/22
def good_match(og:str,ref:list[str]):
    good = ''
    approx = 0
    og = og.lower()
    for target in ref:
        new_approx = fuzz.token_sort_ratio(og,target)
        if new_approx > approx:
            approx = new_approx
            good = target
    if approx < 60:
        good = og
    return good
def polish(df):
    # remove \r characters
    df = df.rename(lambda s:s.replace('\r',' '),axis='columns') # remove '\r' from headers
    df = df.replace('\r','',regex=True) # replace all '\r' throughout
    # approximate headers
    cols = df.columns
    newcols = [good_match(col,conf.CANON_HEADERS) for col in cols]
    df.columns = newcols
    return df
def overflow_check(df,ref,main_df):
    head = df.head(10) # Can set this to be the necessary number of rows -- typically overflow only lasts for 2-3 rows
    headers_at = 0
    for row in range(len(head)):
        if sum([bool(any([fuzz.token_sort_ratio(cell,target) > 60 for target in ref])) for cell in head.loc[row]]) < 2: # if there are less than 2 near-canonical headers
            if sum([bool(any([fuzz.token_sort_ratio(cell,target) > 60 for target in ref])) for cell in head.loc[row]]) > 4: # if there are more than 4 near-canonical headers in the row
                headers_at = row
                overflow = df.columns.values
                df = polish(df)
                overflow = pd.DataFrame(overflow,columns = ref)
                main_df = main_df.append(overflow,ignore_index=True)
                df = df.loc[:headers_at+1]
            df = polish(df)
            df.loc[headers_at,'audit observation'] = '!PHIL EXCEPTION: Dataframe columns are faulty and data has been lost. Refer to the document to find the source of error and report the bug in the repository: https://github.com/hudnash/phil/issues'
def extract(di):
    target_page = -1
    table_end_page = -1
    out = pd.DataFrame()
    file_counter = 1
    for filename in os.listdir(di):
        print('Looking for file n = '+str(file_counter)+'...')
        no_df_found = True
        if os.path.splitext(filename)[1] == ".pdf":
            filename = os.path.join(di,filename)
            print('Now scanning '+filename)
            pdf = p.PdfFileReader(filename)
            page_count = pdf.numPages
            for pagenum in range(page_count):
                print('Looking for Part 3 on p. '+str(pagenum+1)+' of '+str(page_count)+' pages')
                page = pdf.getPage(pagenum)
                page_content = page.extractText()
                if all([target in page_content.lower() for target in conf.TARGET_SENTENCE]):
                    no_df_found = False
                    target_page = pagenum
                    delete_pages_before(filename,target_page)
                    dfs = default(filename) # feed chunks of PDF table scraped via tabula/io.py
                    if len(dfs) > 1:
                        count = 1
                        for df in dfs:
                            print(str(count)+' of '+str(len(dfs))+' dataframes collected.')
                            df = polish(df)
                            overflow_check(df,conf.CANON_HEADERS,out)
                            df = add_filename_col(filename,df) # add a filename column
                            #df = add_location_col(df,filename)
                            #df = add_date_cols(df,filename)
                            out = out.append(df,ignore_index=True) #TODO 11/30/22: Approximate header string matching during append
                            count = count + 1
                    elif len(dfs) == 1:
                        df = add_filename_col(filename,dfs[0])
                        df = polish(df)
                        overflow_check(df,conf.CANON_HEADERS,out)
                        out = out.append(df,ignore_index=True) #TODO 11/30/22: Approximate header string matching during append
                        print('1 of 1 dataframe collected.')
        if no_df_found:
            print('Exception: Could not locate tables in file #'+str(file_counter)+' '+filename+'\nTry: Adjust target sequences list in config.py')
        file_counter = file_counter + 1
    return out