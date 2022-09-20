#!/usr/bin/env python3A
# -*- coding: utf-8 -*-
"""
CLEAN.PY

Created on Thurs June 23, 2022 at 5:50 PM

@author: hudsonnash
"""

from zipfile import ZipFile
import os
from shutil import rmtree
import subprocess
import PyPDF2 as p
import config as c
import mksheet as s
import pandas as pd
from difflib import SequenceMatcher
def unzip(diz,diu):
    z_list = [os.path.join(diz,f) for f in os.listdir(diz) if os.path.isfile(os.path.join(diz,f)) and f[0] != '.']
    for z in z_list:
        with ZipFile(z, 'r') as src:
            src.extractall(diu)
def keep_only_pages_after(filename,start_page):
    infile = p.PdfReader(filename, 'rb')
    pages_to_keep = range(start_page, infile.numPages) # page numbering starts from 0
    output = p.PdfWriter()
    for i in pages_to_keep:
        page = infile.pages[i] 
        output.add_page(page)
        with open(filename, 'wb') as f:
            output.write(f)
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def col_fn(fn,df):
    df['Filename']=[fn for row in range(len(df))]
    return df[['Filename']+[col for col in df if col not in ['Filename']]]
def replace_col(col_name_new,col_name_old):
    #TODO
    pass
def extract(di):
    # search for the correct page and file to begin extraction
    target_page = -1
    table_end_page = -1
    out = pd.DataFrame()
    file_counter = 1
    for filename in os.listdir(di):
        print('Looking for file n = '+str(file_counter)+'...')
        if os.path.splitext(filename)[1] == ".pdf":
            filename = os.path.join(di,filename)
            print('Now scanning '+filename)
            pdf = p.PdfFileReader(filename)
            page_count = pdf.numPages
            only_one_df = True
            no_df_found = True
            for pagenum in range(page_count-1):
                print('Scanning '+str(pagenum+1)+' of '+str(page_count)+' pages')
                page = pdf.getPage(pagenum)
                page_content = page.extractText()
                #print(page_content)
                # print(page_content.lower())
                if all([i in page_content.lower() for i in c.TARGET_SENTENCE]):
                    no_df_found = False
                    target_page = pagenum
                    keep_only_pages_after(filename,target_page)
                    dfs = s.default(filename) # feed chunks of PDF
                    if len(dfs) > 1:
                        for df in dfs:
                            df = col_fn(filename,df) # rename columns
                            print('One dataframe added of multiple')
                            print(df['Audit Observation'])
                            out = out.append(df,ignore_index=True)
                            print('Output in main little loop:')
                            print(out['Audit Observation'])
                            only_one_df = False
                        #df = manual_merge(dfs) #TODO)
                    elif len(dfs) == 1 and only_one_df:
                        df = col_fn(filename,dfs[0])
                        out = out.append(df)
                        print('One dataframe added')
                        print(df['Audit Observation'])
                        print('Single DF in file')
        if no_df_found:
            error('Could not locate tables in file n = '+file_counter+' -- adjust target sequences list in config.py')
        file_counter = file_counter + 1
        print('Final output:')
    print(out['Audit Observation'])
    return out
                    
def manual_merge(dfs):
    cols = 0 #TODO
    for df in dfs:
        if this == this:
            that = 0
    #TODO
def rem_unwanted_data(di):
    # remove all of the files in ../data/unzipped not necessary for mkspreadsheet.py
    # depending on audit format
    uz_list = [os.path.join(di,f) for f in os.listdir(di)]
    for f in uz_list:
        # print(f) # monitor removed files
        if os.path.splitext(f)[1] != '.doc':
            if os.path.isfile(f):
                os.remove(f)
            else:
                rmtree(f)
    # remove all folders in ../data/zipped that make phil fat
    di = os.path.join(os.path.dirname(di),'zip')
    z_folders_list = [os.path.join(di,f) for f in os.listdir(di)]
    for f in z_folders_list:
        try:
            rmtree(f)
        except:
            pass
if __name__ == '__main__':
    _dir = os.path.dirname(os.path.dirname(__file__))
    zipped_dir = os.path.join(_dir,'data','zip')
    unzipped_dir = os.path.join(_dir,'data','unzipped')
    unzip(zipped_dir,unzipped_dir)
    rem_unwanted_data(unzipped_dir)
    # page_content = default_table_search(unzipped_dir)
    # running the convert.sh bash script doesn't work when done in Python:
    # subprocess.Popen('bash convert.sh ../data/unzipped',shell=True)
    # therefore, it should be run separately
