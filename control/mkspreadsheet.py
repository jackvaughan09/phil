#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MKSPREADSHEET.PY

Created on Wed Jun 22 12:25:52 2022

@author: hudsonnash
"""

import os
import pandas as pd
import tabula as t
def table_from_txt(udir):
    for file in os.listdir(udir):
        if os.path.splitext(file)[1] == '.pdf':
            table = t.read_pdf(os.path.abspath(file))
            #TODO: This generates an error (FILE CANNOT BE FOUND ERROR)
    return table
if __name__ == '__main__':
    df = table_from_txt(os.path.join(os.path.dirname(os.getcwd()),'data/unzipped'))
