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
            contents = []
            with open(os.path.join(udir,f),'r') as fobj:
                contents = fobj.read().splitlines()
            prev_row = 0
            row = 0
            row_list = []
            matrix = []
            col = 0
            cell = ''
            for line in contents:
                print(line)
                prev_row = row
                while row == prev_row:
                    for ch in line:
                        if ch == '|':
                            col = col + 1
                        elif ch == '\n':
                            row = row + 1
                            col = 0
                        cell = cell + ch
                    row_list.append(cell)
                    # print(cell)
                matrix.append(row_list)
            frame = matrix # TODO
                    
            # TO CREATE A NEW FILE WITHOUT THE TITLE:
            # os.remove(os.path.join(udir,f))
            # with open(os.path.join(udir,f),'w') as fobj:
                # contents = fobj.writelines(contents[3:])
            
    return frame
if __name__ == '__main__':
    df = table_from_txt(os.
