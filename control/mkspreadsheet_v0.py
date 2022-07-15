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
    frame_dict = {}
    print(os.listdir(udir))
    for txt in os.listdir(udir):
        print('check1')
        base,ext=os.path.splitext(txt)
        print(ext)
        if ext == '.txt':
            print('check2')
            col_num = 0
            frame = pd.DataFrame()
            headers = []
            with open(os.path.join(udir,txt), 'r') as f:
                col = 0
                print('check3')
                print(txt)
                print(os.path.join(udir,txt))
                lines = f.readlines()
                print(lines[1])
                for line in lines:
                    print('check3.5')
                    print(line)
                    print(headers)
                    if line > '':
                        if line[0] == '+' or line[0] == '-':
                            print('check4')
                            # divider line
                            for char in line:
                                if char == '+':
                                    print('check5')
                                    col_num = col_num + 1
                        elif headers != []:
                            col = 0
                            arr = [i for i in range(col_num)]
                            for char in line:
                                if char == '|':
                                    print('check6')
                                    col = col + 1
                                else:
                                    print('check7')
                                    arr[col] = arr[col] + char
                            frame = frame.append(pd.Series(arr),ignore_index=True)
                            print(frame)
                        elif headers == []:
                            print('check8')
                            char = 0
                            while col < col_num:
                                if char == '|':
                                    print('check9')
                                    col = col + 1
                                else:
                                    print('check10')
                                    headers[col] = line[:line[char:].index('|')]
                                    char = char + 1
                            frame.columns = headers
            frame_dict.update({'cityyear':base[base.index('-'):base.index('_')],
                               'data':frame
                               })
    return frame_dict
if __name__ == '__main__':
    print(table_from_txt('/Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/data/unzipped'))
    