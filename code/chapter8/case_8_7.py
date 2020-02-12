# -*- coding: utf-8 -*-
import os
import os.path
import shutil
import zipfile
"""this is a example for chapter 7 file and dir"""
#定义项目备份函数
def proBaker(bpath,blist):
    targetDir=os.path.normpath(bpath)
    (upDir,proName)=os.path.split(targetDir)
    dirName=proName+'_bak'
    bakDir=os.path.join(upDir,dirName)
    modelDir=os.path.join(bakDir,'Models')
    reporDir=os.path.join(bakDir,'reports')
    datasDir=os.path.join(bakDir,'datas')
    otherDir=os.path.join(bakDir,'others')
    #下面几行用来建立用于存放有用文件的目录
    #bakDir和其子目录modelDir，reporDir。。。
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
    #生成索引文件finfor和zip压缩文件。
    finfor=open(inforName,'w')
    newZip=zipfile.ZipFile(zipName,'w')
    for root,dirs,files in os.walk(targetDir):
        for file0 in files:
            fileExten=os.path.splitext(os.path.basename(file0))[1][1:]
            for i in range(len(blist)):
                if blist[i].count(fileExten)>0:
                    #判断成立时将当前文件需要备份到目标目录并添加到压缩文件中
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