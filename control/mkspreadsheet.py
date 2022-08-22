#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MKSPREADSHEET.PY

Created on Wed Jun 22 12:25:52 2022

@author: hudsonnash
"""
import os
import tabula as tab
import re
import pandas as pd

def lamitan(udir):
    for file in os.listdir(udir):
        if os.path.splitext(file)[1] == '.pdf':
            dfs = tab.read_pdf(os.path.join(udir,file),lattice=True,pages='all')
            return pd.concat(dfs)
if __name__ == '__main__':
    # TODO : Classify the document as Lamitan format or Garden City format
    df = lamitan(os.path.join(os.path.dirname(os.getcwd()),'data/unzipped'))
    df.to_excel('test.xlsx')
    
