#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MKSHEET.PY

Created on Wed Jun 22 12:25:52 2022

@author: hudsonnash
"""

from pandas import DataFrame
from extracttools import extract
import sys
from datetime import date
import os

def get_new_wb_name():
    return date.today().strftime("%B %d, %Y")

def mv_to_pdf_folder(di,ndi):
    for file in os.listdir(di):
        if 'pdf' in os.path.splitext(file)[1].lower():
            os.rename(os.path.join(di,file),os.path.join(ndi,os.path.basename(file)))
            print(file,ndi)

if __name__ == '__main__':
    data_url = sys.argv[1]
    print(data_url)
    new_data_url = '../data/pdf'
    mv_to_pdf_folder(data_url,new_data_url)
    data_url = new_data_url
    df = extract_all(data_url)
    if not os.path.exists('../data/xlsx'):
        os.mkdir('../data/xlsx')
    df.to_excel('../data/xlsx/'+get_new_wb_name()+'.xlsx')
