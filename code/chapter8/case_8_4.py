# -*- coding: utf-8 -*-
"""this is a example for chapter 8 file and dir"""
import os
import os.path
#��ʾ��ǰ�ļ����ڵ�Ŀ¼
currdir=os.getcwd()
print type(currdir)
print 'Current work dir is: '+currdir
fatherdir=os.path.dirname(currdir)
print 'Father dir is: '+fatherdir
#�г���ǰ�ļ���һ��Ŀ¼�µ��ļ���Ŀ¼
#������Ϣ��¼���ļ�dir.txt��
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