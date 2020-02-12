# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

Ra = 10.0
Rb = 20.0
Ha = 20.0
Hb = 10.0

myModel = Mdb().Model(name='ModelCompress', modelType=STANDARD_EXPLICIT)

s0 = myModel.ConstrainedSketch(name='specimen', sheetSize=200.0)
s0.sketchOptions.setValues(viewStyle=AXISYM)
s0.setPrimaryObject(option=STANDALONE)
s0.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s0.rectangle(point1=(0.0, 0.0), point2=(Ra, Ha))
pSpeci = myModel.Part(name='specimen', dimensionality=AXISYMMETRIC, 
    type=DEFORMABLE_BODY)
pSpeci.BaseShell(sketch=s0)
s0.unsetPrimaryObject()
s1 = myModel.ConstrainedSketch(name='punch', sheetSize=200.0)
s1.sketchOptions.setValues(viewStyle=AXISYM)
s1.setPrimaryObject(option=STANDALONE)
s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s1.rectangle(point1=(0.0, Ha), point2=(Rb, Ha + Hb))
pPunch = myModel.Part(name='punch', dimensionality=AXISYMMETRIC, 
    type=DEFORMABLE_BODY)
pPunch.BaseShell(sketch=s1)
s1.unsetPrimaryObject()
mat1 = myModel.Material(name='steel')
mat1.Elastic(table=((210000.0, 0.3), ))
mat2 = myModel.Material(name='Alu')
mat2.Elastic(table=((70000.0, 0.33), ))
mat2.Plastic(table=((180.0, 0.0), (200.0, 0.2)))
myModel.HomogeneousSolidSection(name='SectSteel', 
    material='steel', thickness=None)
myModel.HomogeneousSolidSection(name='SectAlu', 
    material='Alu', thickness=None)
f = pSpeci.faces
region = regionToolset.Region(faces=f)
pSpeci.SectionAssignment(region=region, sectionName='SectAlu')
f = pPunch.faces
region = regionToolset.Region(faces=f)
pPunch.SectionAssignment(region=region, sectionName='SectSteel')

root = myModel.rootAssembly
root.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0),
    point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
instP = root.Instance(name='Punch', part=pPunch, dependent=ON)
instS = root.Instance(name='Speciman', part=pSpeci, dependent=ON)

e1 = instP.edges
edges1 = e1.findAt(((Rb/2.0, Ha + Hb, 0.0),),)
pushSet = root.Set(edges=edges1, name='Set-Push')
edges2 = e1.findAt(((Rb/2.0, Ha, 0.0),),)
contPunch = root.Surface(side1Edges=edges2, name='Surf-up')
e1 = instS.edges
edges1 = e1.findAt(((Ra/2.0, 0.0, 0.0),),)
fixSet = root.Set(edges=edges1, name='Set-Fix')
edges2 = e1.findAt(((Ra/2.0, Ha, 0.0),),)
contSpeci = root.Surface(side1Edges=edges2, name='Surf-down')

myStep = myModel.StaticStep(name='Step-1', previous='Initial', nlgeom=ON,
    maxNumInc=1000, initialInc=0.1, minInc=1e-06, maxInc=0.4)
myModel.fieldOutputRequests['F-Output-1'].setValues(numIntervals=10)
myStep.Restart(frequency=0, numberIntervals=10, overlay=OFF, timeMarks=ON)

myModel.ContactProperty('IntProp-1').TangentialBehavior(
    formulation=PENALTY, table=((0.2, ), ), fraction=0.005)
myModel.SurfaceToSurfaceContactStd(name='Int-1', createStepName='Step-1',
    master=contPunch, slave=contSpeci, sliding=FINITE, thickness=ON, 
    interactionProperty='IntProp-1')

fixBC = myModel.DisplacementBC(name='BC-Fix', createStepName='Initial', 
    region=fixSet, u2=SET, ur3=SET)
pushBC = myModel.DisplacementBC(name='BC-Push', createStepName='Initial', 
    region=pushSet, u1=SET, u2=SET, ur3=SET)
pushBC.setValuesInStep(stepName='Step-1', u2=-4.0)

pPunch.seedPart(size=0.5, deviationFactor=0.1)
elemType1 = mesh.ElemType(elemCode=CAX4R, elemLibrary=STANDARD, 
    hourglassControl=ENHANCED)
elemType2 = mesh.ElemType(elemCode=CAX3, elemLibrary=STANDARD, 
    hourglassControl=ENHANCED)
f = pPunch.faces
pPunch.setElementType(regions=(f,), elemTypes=(elemType1, elemType2))
pPunch.generateMesh()
pSpeci.seedPart(size=0.5, deviationFactor=0.1)
f = pSpeci.faces
pSpeci.setElementType(regions=(f,), elemTypes=(elemType1, elemType2))
pSpeci.generateMesh()
root.regenerate()

mdb.Job(name='Data4Transfer', model='ModelCompress', type=ANALYSIS,
    multiprocessingMode=DEFAULT, numCpus=1)
#mdb.jobs['Data4Transfer'].submit(consistencyChecking=OFF)
#: The job input file "Punch1.inp" has been submitted for analysis.