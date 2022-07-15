#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHIL.PY (DRIVER FILE)

Created on Wed Jun  1 10:30:33 2022

@author: hudsonnash
"""

from zipfile import ZipFile
import os.path
from shutil import rmtree, copytree
import subprocess
from stat import S_IWUSR, S_IREAD, S_IXUSR
import pandas as pd
from textract import process
# import textract

def unzip(diz,diu):
    z_list = [os.path.join(diz,f) for f in os.listdir(diz) if os.path.isfile(os.path.join(diz,f)) and f[0] != '.']
    for z in z_list:
        with ZipFile(z, 'r') as src:
            src.extractall(diu)
def rem_unwanted_data(di):
    uz_list = [os.path.join(di,f) for f in os.listdir(di)]
    print(uz_list)
    for f in uz_list:
        if os.path.basename(f)[:2] != '02':
            if os.path.isfile(f):
                os.remove(f)
            else:
                rmtree(f)
def straight_convert_file_type(di):
    uz_list = [os.path.join(di,f) for f in os.listdir(di)]
    global content_list
    content_list = {}
    for f in uz_list:
        content_list.update([[f,[]]])
        base,ext=os.path.splitext(f)
        if ext != 'txt':
            os.rename(f,base+'.txt')
        with open(base+'.txt','rb') as readin: # ISO/IEC 8859-1:1998 to unicode
            for line in readin:
                print(line)
                content_list.get(f).append(line.rstrip(b'\x00'))
    print(content_list)
    for i in content_list.keys():
        for j in content_list[i]:
            for k in j:
                if k != 255 and k != 0:
                    print(hex(k))
    return content_list
                
# def on_rm_error( func, path, exc_info):
#     # path contains the path of the file that couldn't be removed
#     # let's just assume that it's read-only and unlink it.
#     os.chmod( path, stat.S_IWRITE )
#     os.unlink( path )
def convert_file_type(di,*pswd):
    # correct output (run this in terminal):
    # /Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/control/!Antiword/!Antiword /Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/data/unzipped/02-LamitanCity2010_Status_of_Prior_Years_Audit_Recommendations.doc > /Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/data/unzipped/02-LamitanCity2010_Status_of_Prior_Years_Audit_Recommendations.txt
    # my_env = os.environ
    # my_env["PATH"] = "/" + my_env["PATH"]
    # subprocess.Popen('/Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/!Antiword', env=my_env)
    # antiword = '/Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/control/!Antiword/!Antiword'
    # os.chmod(antiword, S_IWUSR|S_IREAD|S_IXUSR)
    # os.chdir('!Antiword')
    # print(os.getcwd())
    # os.system('chmod 777 !Antiword')
    # copytree(os.path.dirname(antiword),os.path.abspath('/'))
    uz_list = [os.path.join(di,f) for f in os.listdir(di)]
    # os.chown(antiword, os.geteuid(), os.getegid())
    # os.chdir('/')
    for f in uz_list:
        base,ext=os.path.splitext(f)
        print('**'+f)
        if ext != 'txt':
            # p = subprocess.Popen('echo '+pswrd+' | sudo -S '+antiword+' '+f+' > '+base+'.txt',shell=True,stdout=subprocess.PIPE)
            # p = subprocess.Popen('antiword'+' '+f+' > '+base+'.txt',shell=True,executable='/opt/local/bin/antiword',stdout=subprocess.PIPE)
            # p = subprocess.Popen('antiword '+os.path.join(os.path.dirname(__file__),'/data/unzipped/02-LamitanCity2010_Status_of_Prior_Years_Audit_Recommendations.doc > /Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/data/unzipped/02-LamitanCity2010_Status_of_Prior_Years_Audit_Recommendations.txt'),shell=True,executable='/opt/local/bin/antiword',stdout=subprocess.PIPE)
            p = subprocess.Popen('antiword -m \"/Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/data/unzipped/02-LamitanCity2010_Status_of_Prior_Years_Audit_Recommendations.doc\" > \"/Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/data/unzipped/02-LamitanCity2010_Status_of_Prior_Years_Audit_Recommendations.txt\"',executable='/opt/local/bin/antiword',stdout=subprocess.PIPE)
            # os.system('which ifconfig')
            # os.system('antiword '+f+' > '+base+'.txt')
            # subprocess.check_call(['bash','./aw.sh',f,base+'.txt','G0a1g3tt3r63'],shell=False)
            #global pc
            #pc = p.communicate()
            #for i in pc:
            #    print(i)
            # print(text)
            process(f)          

if __name__ == '__main__':
    _dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    zipped_dir = os.path.join(_dir,'data','zip')
    unzipped_dir = os.path.join(_dir,'data','unzipped')
    unzip(zipped_dir,unzipped_dir)
    rem_unwanted_data(unzipped_dir)
    # convert_file_type(unzipped_dir) 
    # with open('binarytest.txt','wb') as f:
    #     for line in contents['/Users/hudsonnash/Dropbox/Mac/Desktop/philippines_download/data/unzipped/02-LamitanCity2010_Status_of_Prior_Years_Audit_Recommendations.txt']:
    #         print(line)
    print(table_from_txt(unzipped_dir))
   