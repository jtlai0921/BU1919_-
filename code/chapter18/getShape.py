# -*- coding: mbcs -*-
from odbAccess import *

def getShape(odbPath, instName, stepName, frame=1):
    x, y =[], []
    o = openOdb(path=odbPath, readOnly=True)
    ns = o.rootAssembly.instances[instName.upper()].nodes
    fop = o.steps[stepName].getFrame(frameValue=frame).\
        fieldOutputs['U'].values
    for i in range(len(ns)):
        (x1, y1, z1) = ns[i].coordinates
        (u1, u2) = fop[i].data
        x.append(u1 + x1)
        y.append(u2 + y1)
    o.close()
    return x, y

if __name__=='__main__':
    odbPath = 'HangingChain.odb'
    instName = 'therope'
    stepName = 'Step-StressRelease'
    print getShape(odbPath, instName, stepName)