# -*- coding: utf-8 -*-
import sys
import math
import re
import os
import csv

class myMaterial:
    """this is a class to define the optimization material"""

    infor='Author JingheSu, Email:: alwjybai@gmail.com'
    cluster='optimization'

    def __init__ (self,density,elastic,plastic,expansion,specificheat,
                    conductivity):
        self.elastic=elastic
        self.plastic=plastic
        self.expansion=expansion
        self.specificheat=specificheat
        self.conductivity=conductivity
        self.density=density
    
    def setElastic (self,elastic):
        self.elastic=elastic
        
    def setPlastic (self,plastic):
        self.plastic=plastic

    def setExpansion (self,expansion):
        self.expansion=expansion

    def setSpecificheat (self,specificheat):
        self.specificheat=specificheat

    def setConductivity (self,conductivity):
        self.conductivity=conductivity

    def setDensity (self,density):
        self.density=density

    def printInfor (self):
        print self.infor
        print 'this material belongs to set: '+self.cluster

#============================================================

def updateMaterial():
    """this function is used to update the material in current
    directory. with this function you can insert your material
    just by updating your material data using a csv file"""
    csvlist=[]
    cdir=os.getcwd()
    clist=os.listdir(cdir)
    matDict={}
    for item in clist:
        filedir=os.path.join(cdir, item)
        if os.path.isfile(filedir) and str(item).endswith('mat.csv'):
            csvlist.append(filedir)
    if len(csvlist)==0:
        print 'you got no material to use, material collection programm' \
            'exit!'
        return 0
    else:
        for item in csvlist:
            csvreader=csv.reader(file(item))
            tempDensity=[]
            tempElastic=[]
            tempPlastic=[]
            tempExpansion=[]
            tempSpecificheat=[]
            tempConductivity=[]
            for row in csvreader:
                num=len(row)
                templist=[]
                typename=row[0].strip()
                for data in row[1:]:
                    posteddata=data.strip()
                    if posteddata!='':
                        templist.append(float(posteddata))
                if typename=='density':
                    tempDensity.append(templist)
                elif typename=='elastic':
                    tempElastic.append(templist)
                elif typename=='plastic':
                    tempPlastic.append(templist)
                elif typename=='expansion':
                    tempExpansion.append(templist)
                elif typename=='specificheat':
                    tempSpecificheat.append(templist)
                elif typename=='conductivity':
                    tempConductivity.append(templist)
            tempMat=myMaterial(tempDensity,tempElastic,tempPlastic,
                tempExpansion,tempSpecificheat,tempConductivity)
            (filepath, filename) = os.path.split(item) 
            matDict[filename[:-4]]=tempMat

    return matDict
#===========================================================

if __name__ == '__main__':
    result=updateMaterial()
    print len(result)
    print result.values()[0].density
    print result.values()[0].specificheat