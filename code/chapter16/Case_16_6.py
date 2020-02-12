# -*- coding: mbcs -*-
import os, os.path, sys
from odbAccess import *
from abaqusConstants import *

o = openOdb(path='HertzContact.odb', readOnly=False)
a = o.rootAssembly
insts = a.instances
inst1 = insts['BASE-1']
ele1 = inst1.elements
eleLabel1 = [ele.label for ele in ele1]
if a.elementSets.has_key('eleSet1'):
    eleSet1 = a.elementSets['eleSet1']
else:
    eleSet1 = a.ElementSet(name='eleSet1', elements=(ele1,))
frame = o.steps['Contact'].frames[-1]
fopDIY = frame.FieldOutput(name='DIY',description='stress triaxiality',
    type=SCALAR)
fopS = frame.fieldOutputs['S']
fopSFromEle = fopS.getSubset(region=eleSet1).values
ST = [(SFromEle.press/SFromEle.mises if SFromEle.mises>1.0 else 0.0,) 
    for SFromEle in fopSFromEle]
fopDIY.addData(position=CENTROID, instance=inst1, labels=eleLabel1,
    data=ST)
o.close()