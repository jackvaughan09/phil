#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLEAN_DUMP_TO_DIR.PY (DRIVER FILE)

Created on Thurs June 23, 2022 at 5:50 PM

@author: hudsonnash
"""

from zipfile import ZipFile
import os
from shutil import rmtree
import subprocess
def unzip(diz,diu):
    z_list = [os.path.join(diz,f) for f in os.listdir(diz) if os.path.isfile(os.path.join(diz,f)) and f[0] != '.']
    for z in z_list:
        with ZipFile(z, 'r') as src:
            src.extractall(diu)
def rem_unwanted_data(di):
    # remove all of the files in ../data/unzipped not necessary for mkspreadsheet.py
    # depending on audit format
    uz_list = [os.path.join(di,f) for f in os.listdir(di)]
    for f in uz_list:
        print(f)
        if os.path.basename(f)[:2] != '02' or os.path.splitext(f)[1] != '.doc':
            if os.path.isfile(f):
                os.remove(f)
            else:
                rmtree(f)
    # remove all folders in ../data/zipped that make phil fat
    di = os.path.join(os.path.dirname(di),'zip')
    z_folders_list = [os.path.join(di,f) for f in os.listdir(di)]
    for f in z_folders_list:
        try:
            rmtree(f)
        except:
            pass
if __name__ == '__main__':
    _dir = os.path.dirname(os.path.dirname(__file__))
    zipped_dir = os.path.join(_dir,'data','zip')
    unzipped_dir = os.path.join(_dir,'data','unzipped')
    unzip(zipped_dir,unzipped_dir)
    rem_unwanted_data(unzipped_dir)
    # running the convert.sh bash script doesn't work when done in Python:
    # subprocess.Popen('bash convert.sh ../data/unzipped',shell=True)
    # therefore, it should be run separately