# -*- coding: mbcs -*-
import os, os.path, sys
from odbAccess import *
from abaqusConstants import *

o = openOdb(path='HertzContact.odb', readOnly=False)
insts = o.rootAssembly.instances
inst1 = insts['BASE-1']
ele1 = inst1.elements
frame = o.steps['Contact'].frames[-1]
fopDIY = frame.FieldOutput(name='DIY',description='stress triaxiality',
    type=SCALAR)
fopS = frame.fieldOutputs['S']
for ele in ele1:
    SFromEle = fopS.getSubset(region=ele).values[0]
    temp = SFromEle.press/SFromEle.mises if SFromEle.mises>1.0 else 0.0
    fopDIY.addData(position=CENTROID, instance=inst1, labels=[ele.label,],
        data=((temp,),))
o.close()