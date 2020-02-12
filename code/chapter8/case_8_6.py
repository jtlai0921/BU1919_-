# -*- coding: utf-8 -*-
"""this is a example for chapter 7 file and dir"""
import os
import os.path
import zipfile

#获得当前工作目录
currdir=os.getcwd()
#压缩目录下所有文件，生成压缩文件test.zip
infor=os.listdir(currdir)
print 'Before compressed'+str(infor)
newDir=os.path.join(currdir,'test')
zipName=os.path.join(newDir,'test.zip')
try:
    os.mkdir(newDir)
except:
    print 'directory "test" already exist!'
f = zipfile.ZipFile(zipName, 'w' ,zipfile.ZIP_DEFLATED)
for item in infor:
    tempdir=os.path.join(currdir,item)
    if os.path.isfile(tempdir):
        f.write(item)
f.close()
f=zipfile.ZipFile(zipName)
f.extractall(newDir)
print 'After compressed'+str(os.listdir(newDir))
f.close()