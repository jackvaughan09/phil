#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MKSPREADSHEET.PY

Created on Wed Jun 22 12:25:52 2022

@author: hudsonnash
"""

import os
import pandas as pd
def table_from_txt(udir):
    frame = pd.DataFrame()
    for f in os.listdir(udir):
        if f[f.find('.')+1:] == 'txt':
            temp = pd.read_csv(str(os.path.join(udir,f)),sep='|')
            frame = temp
        #TODO: do something with temp to append it to returned frame (if exists)     
    return frame
if __name__ == '__main__':
    df = table_from_txt(os.path.join(os.path.dirname(os.getcwd()),'data/unzipped'))
    df.to_excel(os.path.abspath('../data/xlsx/most_recent_output.xlsx'))
