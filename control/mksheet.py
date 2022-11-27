#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MKSHEET.PY

Created on Wed Jun 22 12:25:52 2022

@author: hudsonnash
"""
import os
import tabula.io as tab
import re
import pandas as pd
import clean as cl
import sys

def default(filename):
    dfs = tab.read_pdf(filename,lattice=True,pages='all') # pages attribute of tabula-py is broken
    return dfs
def lamitan(udir):
    for file in os.listdir(udir):
        if os.path.splitext(file)[1] == '.pdf':
            dfs = tab.read_pdf(os.path.join(udir,file),lattice=True,pages='all')
            return pd.concat(dfs)
if __name__ == '__main__':
    data_url = sys.argv[1]
    print(data_url)
    df = cl.extract(data_url)
    df.to_excel('../data/xlsx/'+input('Type your desired Excel file name: ')+'.xlsx')
