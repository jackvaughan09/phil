#!/usr/bin/env python3A
# -*- coding: utf-8 -*-
"""
CLEAN.PY

Created on Thurs June 23, 2022 at 5:50 PM

@author: hudsonnash
"""

from zipfile import ZipFile
import os
from shutil import rmtree
import PyPDF2 as p
import config as c
import code
from pathlib import Path
import sys

def unzip(diz,diu):
    z_list = [os.path.join(diz,f) for f in os.listdir(diz) if os.path.isfile(os.path.join(diz,f)) and f[0] != '.']
    for z in z_list:
        with ZipFile(z, 'r') as src:
            src.extractall(diu)
def remove_junk(di):
    uz_list = [os.path.join(di,f) for f in os.listdir(di)]
    for f in uz_list:
        has_filename_target = any([target in os.path.splitext(f)[0] for target in c.FILENAME_TARGET])
        is_pdf = bool(os.path.splitext(f)[1]=='.pdf')
        is_doc = bool(os.path.splitext(f)[1] in ['.docx','.doc'])
        print(f'''
        File: 
        {f.split('/')[3]}
        =======================================
        target filename: {has_filename_target}
        pdf:             {is_pdf}
        doc/docx:        {is_doc}
        keep:            {is_doc or (is_pdf and has_filename_target)}
        ''')
        if is_doc and has_filename_target:
            print(f'{f} is doc and has target name')
            continue
        elif is_pdf and has_filename_target:
            print(f'{f} is pdf and has target name')
            continue
        elif os.path.isfile(f):
            print(f'Removing {f}')
            os.remove(f)
        else:
            rmtree(f)
    di = os.path.join(os.path.dirname(di),'zip')
    z_folders_list = [os.path.join(di,f) for f in os.listdir(di)]
    for f in z_folders_list:
        try:
            rmtree(f)
        except:
            pass
if __name__ == '__main__':
    zipped_dir = sys.argv[1]
    unzipped_dir = sys.argv[2]
    unzip(zipped_dir,unzipped_dir)
    remove_junk(unzipped_dir)


# if __name__ == '__main__':
#     _dir = str(Path(__file__).resolve().parents[1])