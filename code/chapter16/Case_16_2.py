# -*- coding: mbcs -*-
import os, os.path, sys
from odbAccess import *
from abaqusConstants import *
def extractNodes(odbname, tname, tpath=None):
    if tpath==None:
        tpath = os.getcwd()
    tname = tname + '.inp'
    oname = odbname+'.odb'
    tFile=os.path.join(tpath,tname)
    oPath=os.path.join(tpath,oname)
    f = open(tFile, 'w')
    o = openOdb(path=oPath)
    instes = o.rootAssembly.instances
    for key in instes.keys():
        labels, xyz = [], []
        for node in instes[key].nodes:
            labels.append(node.label)
            xyz.append(node.coordinates)
        cc = dict(zip(labels, xyz))
        aa = sorted(labels)
        bb = [cc[item] for item in aa]
        f.write('*Instance '+instes[key].name+'\n')
        for i in range(len(aa)):
            tepS = str(aa[i])+', '+str(bb[i][0])+', '+str(bb[i][1])+', '+\
            str(bb[i][2])+'\n'
            f.write(tepS)
    f.close()
    o.close()

if __name__=="__main__":
    extractNodes(odbname='HertzContact', tname='hertzcontact')
