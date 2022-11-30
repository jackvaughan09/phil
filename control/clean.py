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

def unzip(diz,diu):
    z_list = [os.path.join(diz,f) for f in os.listdir(diz) if os.path.isfile(os.path.join(diz,f)) and f[0] != '.']
    for z in z_list:
        with ZipFile(z, 'r') as src:
            src.extractall(diu)
def remove_junk(di):
    uz_list = [os.path.join(di,f) for f in os.listdir(di)]
    for f in uz_list:
        if 'doc' not in os.path.splitext(f)[1] or not any([target in os.path.splitext(f)[0] for target in c.FILENAME_TARGET]):
            if os.path.isfile(f):
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
    _dir = os.path.dirname(os.path.dirname(__file__))
    zipped_dir = os.path.join(_dir,'data','zip')
    unzipped_dir = os.path.join(_dir,'data','unzipped')
    unzip(zipped_dir,unzipped_dir)
    remove_junk(unzipped_dir)
