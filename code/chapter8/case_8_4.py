# -*- coding: utf-8 -*-
"""this is a example for chapter 8 file and dir"""
import os
import os.path
#显示当前文件所在的目录
currdir=os.getcwd()
print type(currdir)
print 'Current work dir is: '+currdir
fatherdir=os.path.dirname(currdir)
print 'Father dir is: '+fatherdir
#列出当前文件上一级目录下的文件和目录
#并将信息记录到文件dir.txt中
f=open('dir.txt','w')
infor=os.listdir(fatherdir)
fileNum=0
dirNum=0
for item in infor:
    tempdir=os.path.join(fatherdir,item)
    if os.path.isdir(tempdir):
        dirNum=dirNum+1
        tempStr='dir: '+tempdir+'\n'
        f.writelines(tempStr)
    elif os.path.isfile(tempdir):
        fileNum=fileNum+1
        tempStr='file: '+tempdir+'\n'
        f.writelines(tempStr)
tempStr1='you get '+str(dirNum)+' dirs in the path.\n'
tempStr2='you get '+str(fileNum)+' files in the path.\n'
f.writelines(tempStr1)
f.writelines(tempStr2)
f.close()