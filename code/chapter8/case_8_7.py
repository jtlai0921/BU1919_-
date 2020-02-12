# -*- coding: utf-8 -*-
import os
import os.path
import shutil
import zipfile
"""this is a example for chapter 7 file and dir"""
#������Ŀ���ݺ���
def proBaker(bpath,blist):
    targetDir=os.path.normpath(bpath)
    (upDir,proName)=os.path.split(targetDir)
    dirName=proName+'_bak'
    bakDir=os.path.join(upDir,dirName)
    modelDir=os.path.join(bakDir,'Models')
    reporDir=os.path.join(bakDir,'reports')
    datasDir=os.path.join(bakDir,'datas')
    otherDir=os.path.join(bakDir,'others')
    #���漸�������������ڴ�������ļ���Ŀ¼
    #bakDir������Ŀ¼modelDir��reporDir������
    try:
        os.mkdir(bakDir)
    except:
        pass
    try:
        os.mkdir(modelDir)
    except:
        pass
    try:
        os.mkdir(reporDir)
    except:
        pass
    try:
        os.mkdir(datasDir)
    except:
        pass
    try:
        os.mkdir(otherDir)
    except:
        pass
    newDirs=[modelDir,reporDir,datasDir,otherDir]
    inforName=os.path.join(bakDir,proName+'.txt')
    zipName=os.path.join(bakDir,proName+'.zip')
    #���������ļ�finfor��zipѹ���ļ���
    finfor=open(inforName,'w')
    newZip=zipfile.ZipFile(zipName,'w')
    for root,dirs,files in os.walk(targetDir):
        for file0 in files:
            fileExten=os.path.splitext(os.path.basename(file0))[1][1:]
            for i in range(len(blist)):
                if blist[i].count(fileExten)>0:
                    #�жϳ���ʱ����ǰ�ļ���Ҫ���ݵ�Ŀ��Ŀ¼����ӵ�ѹ���ļ���
                    filePath=os.path.join(root,file0)
                    shutil.copy(filePath,newDirs[i])
                    newPath=os.path.join(newDirs[i],file0)
                    finfor.writelines('zip:'+newPath+'\n')
                    newZip.write(newPath)
    finfor.close()
    newZip.close()
				
if __name__=="__main__":
    targetDir=os.getcwd()
    saveList=(('inp','py'),('pptx','docx'),('fil','xlsx','csv'),('txt'))
    proBaker(targetDir,saveList)