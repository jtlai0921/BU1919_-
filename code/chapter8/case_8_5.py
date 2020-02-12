# -*- coding: utf-8 -*-
"""this is a example for chapter 8 file and dir"""
import os
import os.path
import shutil

targetStr='D:/abaqus_workspace/tire_project'
#��ʾ��ǰ����Ŀ¼
currdir1=os.getcwd()
print 'Current work dir before change is: '+currdir1
#��ʾ�л���Ĺ���Ŀ¼
os.chdir(targetStr)
currdir2=os.getcwd()
print 'Current work dir after change is: '+currdir2

#����ǰ�ļ��У�������Ϣ��¼��record.txt�ļ�
#ɾ��.dat,.sta,.msg,.log,.rpy,.prt,.sim,ipm�ļ�
#�ƶ�inp,odb,cae,fil�ļ����½����ļ���test�С�
newDir=os.path.join(currdir2,'test')
try:
    os.mkdir(newDir)
except:
    print 'directory "test" already exist!'
infor=os.listdir(currdir2)
f=open('record.txt','w')
for item in infor:
    tempdir=os.path.join(currdir2,item)
    extStr=os.path.splitext(item)[1]
    if os.path.isfile(tempdir):
        if extStr=='.inp' or extStr=='.cae' or extStr=='.odb' or extStr=='.fil':
            shutil.move(tempdir,newDir)
            tempStr='file '+item+' moved!\n'
        else:
            try:
                os.remove(tempdir)
                tempStr='file '+item+' deleted!\n'
            except:
                tempStr='record.txt '+' remained for search!\n'
        f.writelines(tempStr)
f.close()