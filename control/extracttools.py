import tabula.io as tab
import pandas as pd
from difflib import SequenceMatcher
import PyPDF2 as p
import os
from typing import List
def default(filename,pages):
    dfs = tab.read_pdf(filename,lattice=True,pages=pages) # pages attribute of tabula-py is broken
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
def polish(df: pd.DataFrame) -> pd.DataFrame:
    # remove \r characters
    df = df.rename(lambda s:s.replace('\r',' '),axis='columns') # remove '\r' from headers
    df = df.replace('\r','',regex=True) # replace all '\r' throughout
    # approximate headers
    cols = df.columns
    newcols = [good_match(col,conf.CANON_HEADERS) for col in cols]
    df.columns = newcols
    return df
def is_header(row):
    if sum([bool(any([fuzz.token_sort_ratio(cell,target) > 60 for target in ref])) for cell in head.loc[row]]) < 2:
        """ nonsense case -> treat as overflow """
        return True
    else:
        return False
def separate_overflow(df,ind,page_range) -> list[pd.DataFrame]:
    if is_header(df.columns):
        return [df]
    else:
        # step 1 - find where table actually begins
        start = 0
        for row in range(len(df)):
            if is_header(df.loc[row]):
                start = row
        if start == 0:
            if not is_header(df.loc[0]):
                if not df.empty: # case 2: no row resembling a header found
                    df.columns = conf.CANON_HEADERS # could result in mismatched headers
                    raise(BaseException('Could result in mismatched headers on p.'+str(int(page_range.split('-')[0])+ind)))
        overflow = df.loc[0:start]
        df.drop([i for i in range(0,start)])
        df.columns = df.loc[start]
        df.reset_index()
        return [df,overflow]
def fix_overflow(dfs: list[pd.DataFrame],page_range: str) -> list[pd.DataFrame]:
    for i,df in enumerate(dfs[1:]):
        [df,overflow] = separate_overflow(df,i,page_range)
        # if sum([col != '' for col in overflow]) <= 2: # merging with last row on prev page TODO
        if 0 == sum([s in overflow['observations and recommendations'][0] for s in conf.BULLET_STRS],[s in overflow['audit observation'][0] for s in conf.BULLET_STRS]):
            dfs[i-1].loc[-1] += overflow
        dfs[i-1].append(overflow)
    return dfs
def overflow_check_and_correct(df,ref,main_df):
    head = df.head(10)
    headers_at = 0
    for row in range(len(head)):
        if sum([bool(any([fuzz.token_sort_ratio(cell,target) > 60 for target in ref])) for cell in head.loc[row]]) < 2:
            """ nonsense case -> treat as overflow """
            headers_at = row
            overflow = df.columns.values
            df = polish(df)
            overflow = pd.DataFrame(overflow,columns = ref)
            main_df = main_df.append(overflow,ignore_index=True)
            df = df.loc[:headers_at+1]
        if sum([bool(any([fuzz.token_sort_ratio(cell,target) > 60 for target in ref])) for cell in head.loc[row]]) > 4:
            """ actual header case -> remap them """
            df = polish(df)
        df.loc[headers_at,'audit observation'] = '!PHIL EXCEPTION: Dataframe columns are faulty and data has been lost. Refer to the document to find the source of error and report the bug in the repository: https://github.com/hudnash/phil/issues'
def longest_seq(li: list):
    longest = []
    seq = [li[0]]
    longest_streak = 0
    streak = 0
    for i in range(len(li)-1):
        if li[i] == li[i+1]-1:
            seq = seq + [li[i+1]]
            streak = streak + 1
        else:
            streak = 0
            seq = [li[i+1]]
        if longest_streak < streak:
            longest_streak = streak
            longest = seq
    return longest
def get_pg_rng(pdf_url):
    pdf = p.PdfFileReader(pdf_url)
    n = pdf.numPages
    outp = ''
    pgs = list()
    for pg in range(n):
        page = pdf.getPage(pg)
        content = page.extractText()
        if all([target in content.lower() for target in conf.TARGET_SENTENCE]):
            pgs = pgs + [pg]
    if len(pgs) < 1:
        print('Warning: No pages contain tables: '+pdf_url)
        return '0'
    elif len(pgs) < 2: 
        pgs = [pg for pg in range(pgs[0],n)]
        print('Warning: Only 1 page was detected containing target title')
        return str(min(pgs)+1) + '-' + str(max(pgs)+1)
    elif longest_seq(pgs) == []:
        print('Warning: May have missed a document')
        return '0' # when this occurred, it was the wrong table
    else:
        pgs = longest_seq(pgs) # assume that the area with the most instances of the target sequence words
                           # is where Part IV actually begins as opposed to some front matter or table of contents
        pgs = [pg for pg in range(pgs[0],n)] # scrape starting from official beginning of Part IV until the end of the document
        return str(min(pgs)+1) + '-' + str(max(pgs)+1)
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
            for pagenum in range(page_count): # PROBLEM #TODO 
                print('Looking for Part 3 on p. '+str(pagenum+1)+' of '+str(page_count)+' pages')
                page = pdf.getPage(pagenum)
                page_content = page.extractText()
                if all([target in page_content.lower() for target in conf.TARGET_SENTENCE]):
                    no_df_found = False
                    target_page = pagenum
                    delete_pages_before(filename,target_page) # PROBLEM #TODO: REPETITION OF ROWS OF DATA. This could likely be fixed by setting pages = "1" in tab.read_pdf in default(..).
                    print('!!! PAGENUM: '+str(pagenum))
                    dfs = default(filename,str(pagenum+1)) # feed chunks of PDF table scraped via tabula/io.py
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
def city(df:pd.DataFrame,pdf_url:str)->pd.DataFrame:
    df = df.assign(city=''.join([c for c in ((pdf_url.split('/')[-1])[2:].split('_'))[0].replace('-','') if ord(c) >= 65]))
    for cell in df['city']:
        if cell in list(conf.ABBREV_CITY_NAMES.keys()):
            df = df.assign(city = conf.ABBREV_CITY_NAMES[cell])
    return df
def year(df:pd.DataFrame,pdf_url:str)->pd.DataFrame:
    return df.assign(year=''.join([c for c in ((pdf_url.split('/')[-1])[2:].split('_'))[0].replace('-','') if ord(c) < 65]))