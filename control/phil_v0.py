#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHIL.PY (DRIVER FILE)

Created on Wed Jun  1 10:30:33 2022

@author: hudsonnash
"""

# 1. IMPORTS
from requests import get
from zipfile import ZipFile
from cloudscraper import create_scraper
import os
import pandas as pd
import shlex
from docx import Document
from tabulate import tabulate

# 2. METHODS
# 2.1. GET/SCRAPE METHOD
# TODO
ex = 'https://www.coa.gov.ph/download/4788/basilan/63360/lamitan-city-annual-audit-report-2010.zip'
rq = get(ex,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36','email':'hudsonnash@utexas.edu'})
file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data/zip',rq.url[ex.rfind('/')+1:])
#for chunk in rq.iter_content(chunk_size=1024):
# 2.2. UNPACK ZIP
#def extract_zip_files(d):
z_list = [os.path.join(os.path.dirname(file_name),f) for f in os.listdir(os.path.dirname(file_name)) if os.path.isfile(os.path.join(os.path.dirname(file_name),f)) and f[0] != '.']
for z in z_list:
    with ZipFile(z, 'r') as src:
        src.extractall(os.path.join(os.path.dirname(os.path.dirname(file_name)),'unzipped'))
# 2.3. DELETE UNNECESSARY FILES
file_name = file_name.replace(file_name[file_name.index('/data/zip'):],'')
file_name = os.path.join(file_name,'data','unzipped')
uz_list = [os.path.join(file_name,f) for f in os.listdir(file_name)]
for f in uz_list:
    if os.path.basename(f)[:2] != '02':
        os.remove(f)
        
# 2.4. CONVERT DOC TO TXT
for f in os.listdir(file_name):
    if f[f.index('.'):] == '.txt':

# 2.5. EXTRACT TABULATED DATA FROM DOCX FILES
for f in os.listdir(file_name):
    if f[f.index('.'):] == '.docx':
        doc = Document(os.path.join(file_name,f))
        contents = [[[cell.text for cell in j.cells] for j in i.rows] for i in doc.tables]
        
# 2.6. REORGANIZE TABLE CONTENTS INTO DATAFRAME
main_df = pd.DataFrame()
for table in contents:
    df = pd.DataFrame()
    for row_index in range(len(table)):
        if row_index != 0:
            df = df.append(pd.Series(table[row_index]),ignore_index=True)
    df.columns = table[0]
    main_df = main_df.append(df,ignore_index=False)
print(main_df)
chanmain_df.to_excel('test.xlsx')

# 2.7. EXPORT REORGANIZED DATAFRAME TO EXCEL

# 2.8. RASTER AND REFORMAT WITHIN EXCEL FILE(S)
# TODO

# 2.9. PYTHON ANALYTICS & DATA ADDITIONS
# TODO: NEED GUIDANCE
        
   