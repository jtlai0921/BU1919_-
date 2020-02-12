# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *

mdb = openMdb(pathName='Test.cae')#打开在当前工作目录下的模型Test.cae
vp = session.viewports['Viewport: 1']
o = mdb.models['myModel'].rootAssembly
insts = o.instances
inst1 = o.instances['Part-1-1']
inst2 = o.instances['Part-1-2']
inst3 = o.instances['Part-2-1']
p1 = mdb.models['myModel'].parts['Part-1']
p2 = mdb.models['myModel'].parts['Part-2']
vp.setValues(displayedObject=p1)

es1 = p1.edges
e1 = es1.getByBoundingBox(xMin=-1,xMax=1,yMin=-1,yMax=20,zMin=-1,zMax=25)
eSetFromBox = p1.Set(name='eSetFromBox', edges=e1)
e2 = es1.findAt(((0.0,15.0,10.0),),((15.0,15.0,10.0),))
eSetFromFind = p1.Set(name='eSetFromFind', edges=e2)

fs1 = p2.faces
f1 = fs1.getByBoundingCylinder(center1=(0,-5,0),center2=(0,20,0),radius=8)
fSetFromCylinder = p2.Set(name='fSetFromCylinder', faces=f1)
r1, r2 = 5.0, 15.0
center1 = (r1*sin(pi/6), 7.5, r1*cos(pi/6))
center2 = (r2*sin(pi/6), 7.5, r2*cos(pi/6))
f2 = fs1.findAt((center1,),(center2,))
fSetFromFin = p2.Set(name='fSetFromFind', faces=f2)

cs1 = inst1.cells
cs2 = inst2.cells
cs3 = inst3.cells
c1 = cs1.findAt(((7.5,22.5,20.0),),)
type(c1)
center = (0,0,0)
c2 = cs2.getByBoundingSphere(center=center, radius=50)
c3 = cs3.getByBoundingSphere(center=center, radius=50)
cSet1 = o.Set(name='cSet1', cells=c1+c2+c3)
c0 = cs1.findAt((7.5,22.5,20.0),)
type(c0)
cSet2 = o.Set(name='cSet2', cells=[c0,]+c2+c3)