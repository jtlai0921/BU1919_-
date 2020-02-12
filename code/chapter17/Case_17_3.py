# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
#++++++++++++++++++++++++++++++++++++++17.2
mdb = openMdb(pathName='Test.cae')#打开在当前工作目录下的模型Test.cae
vp = session.viewports['Viewport: 1']
p1 = mdb.models['myModel'].parts['Part-1']
vp.setValues(displayedObject=p1)

es = p1.edges
pt1 = p1.DatumPointByCoordinate(coords=(0.,15.,10.))
e1 = es.findAt((15.,15.,10.),)
pt2 = p1.DatumPointByEdgeParam(edge=e1,parameter=0.5)
pt3 = p1.DatumPointByEdgeParam(edge=e1,parameter=0.2)
pt4 = p1.DatumPointByEdgeParam(edge=e1,parameter=0.8)
e2 = es.findAt((15.,0.,10.),)
pt5 = p1.InterestingPoint(edge=e2, rule=MIDDLE)
d = p1.datums
print type(pt1), type(d[pt1.id]), type(pt5)
PL1 = p1.DatumPlaneByThreePoints(point1=d[pt1.id], point2=d[pt2.id], point3=pt5)
PL2 = p1.DatumPlaneByThreePoints(point1=d[pt1.id], point2=d[pt3.id], point3=pt5)
PL3 = p1.DatumPlaneByThreePoints(point1=d[pt1.id], point2=d[pt4.id], point3=pt5)

cs = p1.cells
myCArray = [cs[0],]
print type(cs), type(myCArray)
p1.PartitionCellByDatumPlane(cells=myCArray, datumPlane=d[PL1.id])
p1.PartitionCellByDatumPlane(cells=cs, datumPlane=d[PL2.id])
fs = p1.faces
pt6 = p1.DatumPointByMidPoint(point1=d[pt1.id], point2=d[pt4.id])
f1 = [fs.findAt(d[pt6.id].pointOn,),]
f2 = fs.findAt((d[pt6.id].pointOn,),)
p1.PartitionFaceByDatumPlane(faces=f1, datumPlane=d[PL3.id])

#++++++++++++++++++++++++++++++++++++++17.3
from abaqus import *
from abaqusConstants import *
from caeModules import *
mdb = openMdb(pathName='Test.cae')#打开在当前工作目录下的模型Test.cae
vp = session.viewports['Viewport: 1']
p1 = mdb.models['myModel'].parts['Part-1']
p2 = mdb.models['myModel'].parts['Part-2']
#几何序列
e1 = p1.edges
p1.seedEdgeByNumber(edges=e1,number=20)
p1.seedEdgeByNumber(edges=[e1[0],],number=60)
p1.seedEdgeByNumber(edges=e1[0],number=60)
#TypeError: edges; found Edge, expecting tuple
c1 = p1.cells
region1 = regionToolset.Region(cells=c1)
p1.generateMesh(regions=c1)
#1300 elements have been generated on part: Part-1
p1.generateMesh(regions=region1)
#TypeError: regions; found Region, expecting tuple
p1.generateMesh(regions=[c1[0],])
#1300 elements have been generated on part: Part-1
p1.generateMesh(regions=c1[0])
#TypeError: regions; found Cell, expecting tuple

#Set和Surface对象
mdb = openMdb(pathName='Test.cae')#打开在当前工作目录下的模型Test.cae
p1 = mdb.models['myModel'].parts['Part-1']
p2 = mdb.models['myModel'].parts['Part-2']
c1 = p1.cells
set1 = p1.Set(name='set1', cells=c1)
p1.SectionAssignment(region=set1, sectionName='Section-Steel', offset=0.0, 
     offsetType=MIDDLE_SURFACE, offsetField='', 
     thicknessAssignment=FROM_SECTION)

a = mdb.models['myModel'].rootAssembly
f11 = a.instances['Part-1-1'].faces
f12 = a.instances['Part-1-2'].faces
f21 = a.instances['Part-2-1'].faces
rp = a.ReferencePoint(point=(0.0,0.0,0.0))
rPoints = a.referencePoints
face4Coupling = f21.findAt(((5.0,0.0,5.0),),)
rpSet = a.Set(name='rpSet', referencePoints=[rPoints[rp.id],])
face5C = a.Set(name='face5C', faces=face4Coupling)
rpCoupling = mdb.models['myModel'].Coupling(name='rpCouping',surface=face5C,
    controlPoint=rpSet,influenceRadius=WHOLE_SURFACE,couplingType=KINEMATIC)

face4Contact = f12.findAt(((5.0,0.0,5.0),),)
face5S = a.Surface(name='face5S', side1Faces=face4Contact)
surfContact = mdb.models['myModel'].SurfaceToSurfaceContactStd(name='contact', 
    createStepName='Initial', master=face5S, slave=face5C, sliding=FINITE, 
    thickness=ON, interactionProperty='IntProp-1', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

face4BC = f12.getByBoundingBox(xMin=-1, xMax=25, yMin=-20, yMax=-10, 
    zMin=-1, zMax=25)
set4BC = a.Set(name='set4BC', faces=face4BC)
sur4BC = a.Surface(name='sur4BC', side1Faces=face4BC)
mdb.models['myModel'].DisplacementBC(name='BC-YFix', createStepName='Initial', 
    region=set4BC, u1=UNSET, u2=SET, u3=UNSET, ur1=UNSET,ur2=UNSET,ur3=UNSET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

face4P = f11.findAt(((5.0,30.0,5.0),),)
sur4P = a.Surface(name='set4P', side1Faces=face4P)
mdb.models['myModel'].Pressure(name='LoadPressure', createStepName='myStep1', 
    region=sur4P, distributionType=UNIFORM, field='', magnitude=1.0, 
    amplitude=UNSET)

#Region对象
mdb = openMdb(pathName='Test.cae')#打开在当前工作目录下的模型Test.cae
p1 = mdb.models['myModel'].parts['Part-1']
c1 = p1.cells
region1 = regionToolset.Region(cells=c1)
p1.SectionAssignment(region=region1, sectionName='Section-Steel', offset=0.0, 
     offsetType=MIDDLE_SURFACE, offsetField='', 
     thicknessAssignment=FROM_SECTION)

a = mdb.models['myModel'].rootAssembly
p12 = a.instances['Part-1-2']
p21 = a.instances['Part-2-1']
f12 = p12.faces
f21 = p21.faces
rp = a.ReferencePoint(point=(0.0,0.0,0.0))
rPoints = a.referencePoints
face4Coupling = f21.findAt(((5.0,0.0,5.0),),)
rpRegion = regionToolset.Region(referencePoints=[rPoints[rp.id],])
face4CRn = regionToolset.Region(faces=face4Coupling)
rpCoupling = mdb.models['myModel'].Coupling(name='rpCouping', surface=face4CRn,
    controlPoint=rpRegion,influenceRadius=WHOLE_SURFACE,couplingType=KINEMATIC)

f4 = f12.getByBoundingBox(xMin=-1, xMax=25, yMin=-20, yMax=-10, zMin=-1, zMax=25)
regionY = regionToolset.Region(faces=f4)
mdb.models['myModel'].DisplacementBC(name='BC-YFix', createStepName='Initial', 
    region=regionY, u1=UNSET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)



a = mdb.models['myModel'].rootAssembly
v1 = a.instances['Part-1-1'].vertices
verts1 = v1.getSequenceFromMask(mask=('[#1 ]', ), )
a.Set(vertices=verts1, name='Set-2')
#: The set 'Set-2' has been created (1 vertex).
a = mdb.models['myModel'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#8 ]', ), )
e1 = a.instances['Part-1-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
f2 = a.instances['Part-1-2'].faces
faces2 = f2.getSequenceFromMask(mask=('[#8 ]', ), )
f3 = a.instances['Part-2-1'].faces
faces3 = f3.getSequenceFromMask(mask=('[#10 ]', ), )
a.Set(edges=edges1, faces=faces1+faces2+faces3, name='setX')
#: The set 'setX' has been edited (3 faces, 1 edge).
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
a = mdb.models['myModel'].rootAssembly
region = a.sets['setX']
mdb.models['myModel'].DisplacementBC(name='BC-4', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=82.7489, 
    farPlane=164.912, width=57.7546, height=41.2109, cameraPosition=(-39.1852, 
    103.109, 73.3562), cameraUpVector=(-0.134088, 0.158905, -0.978146))
a = mdb.models['myModel'].rootAssembly
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
a.Surface(side1Faces=side1Faces1, name='Surf-2')
#: The surface 'Surf-2' has been created (1 face).
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='myStep1')
a = mdb.models['myModel'].rootAssembly
region = a.surfaces['Surf-2']
mdb.models['myModel'].Pressure(name='Load-2', createStepName='myStep1', 
    region=region, distributionType=UNIFORM, field='', magnitude=1.0, 
    amplitude=UNSET)