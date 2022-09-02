#!/usr/bin/env python3
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
    print(start_page)
    pages_to_keep = range(start_page, infile.numPages) # page numbering starts from 0
    output = p.PdfWriter()
    for i in pages_to_keep:
        page = infile.pages[i] 
        output.add_page(page)
    print(output)
    with open(filename, 'wb') as f:
        output.write(f)
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def col_fn(fn,df):
    df['Filename']=[fn for row in range(len(df))]
    return df[['Filename']+[col for col in df if col not in ['Filename']]]
def extract(di):
    # search for the correct page and file to begin extraction
    target_page = -1
    table_end_page = -1
    out = pd.DataFrame()
    for filename in os.listdir(di):
        if os.path.splitext(filename)[1] == ".pdf":
            filename = os.path.join(di,filename)
            pdf = p.PdfFileReader(filename)
            page_count = pdf.numPages
            for pagenum in range(page_count):
                page = pdf.getPage(pagenum)
                page_content = page.extractText()
                # print(page_content.lower())
                if all([i in page_content.lower() for i in c.TARGET_SENTENCE]):
                    target_page = pagenum
                    keep_only_pages_after(filename,pagenum)
                    dfs = s.default(filename) # feed chunks of PDF
                    if len(dfs) > 1:
                        for df in dfs:
                            df = col_fn(filename,df)
                        df = manual_merge(dfs)
                        out = out.append(df,ignore_index=True)
                    elif len(dfs) == 1:
                        df = col_fn(filename,dfs[0])
                        out = out.append(df)
    print(out)
    return out
                    
def manual_merge(dfs):
    for df in dfs:
        print(df)                     
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
