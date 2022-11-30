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

def get_new_wb_name(di):
    return date.today().strftime("%B %d, %Y")

if __name__ == '__main__':
    data_url = sys.argv[1]
    print(data_url)
    df = extract(data_url)
    df.to_excel('../data/xlsx/'+get_new_wb_name(data_url)+'.xlsx')
