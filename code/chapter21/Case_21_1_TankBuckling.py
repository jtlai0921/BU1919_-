# -*- coding: mbcs -*-
import re
from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbAccess import *

Hei = 8000.0
Dwall = 1500.0
Hwall = 10.0
Lrib = 400.0
Hrib = 10.0
Prib = [Hei/3.0, Hei/5.0*3.0]
Press = 9800.0*1.0e-9*Hei
inpName = 'Buck'

Mdb()
md = mdb.models['Model-1']
#Part definition
s1 = md.ConstrainedSketch(name='tank', sheetSize=200.0)
s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s1.Line(point1=(0.0, Hei), point2=(Dwall/2.0, Hei))
s1.Line(point1=(Dwall/2.0, Hei), point2=(Dwall/2.0, 0.0))
s1.Line(point1=(Dwall/2.0, 0.0), point2=(0.0, 0.0))
pTank = md.Part(name='tank', dimensionality=THREE_D, type=DEFORMABLE_BODY)
pTank.BaseShellRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
dat = pTank.datums
for posi in Prib:
    idi = pTank.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, 
        offset=posi+Lrib/2.0).id
    fcs = pTank.faces
    pTank.PartitionFaceByDatumPlane(datumPlane=dat[idi], faces=fcs)
    idi = pTank.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, 
        offset=posi-Lrib/2.0).id
    fcs = pTank.faces
    pTank.PartitionFaceByDatumPlane(datumPlane=dat[idi], faces=fcs)
#Materials and Sections
MatP = md.Material(name='Plastic')
MatP.Density(table=((1e-09, ), ))
MatP.Elastic(table=((10000.0, 0.3), ))
MatS = md.Material(name='steel')
MatS.Density(table=((1e-09, ), ))
MatS.Elastic(table=((200000.0, 0.3), ))
md.HomogeneousShellSection(name='Section-wall', thickness=Hwall,
    preIntegrate=ON, material='Plastic', thicknessType=UNIFORM)
md.HomogeneousShellSection(name='Section-rib', thickness=(Hwall+Hrib),
    preIntegrate=ON, material='Plastic', thicknessType=UNIFORM)
md.HomogeneousShellSection(name='Section-cov', thickness=16.0,
    preIntegrate=ON, material='steel', thicknessType=UNIFORM)
points = []
fcs = pTank.faces
for yi in Prib:
    points.append(((-Dwall/2.0, yi, 0.0),))

faces = fcs.findAt(*points)
ribSet = pTank.Set(name='ribs', faces=faces)
pTank.SectionAssignment(region=ribSet, sectionName='Section-rib')
points = []
offSet = Lrib/2.0+1.0
for yi in Prib:
    points.append(((-Dwall/2.0, yi-offSet, 0.0),))

points.append(((-Dwall/2.0, Hei-offSet, 0.0),))
faces = fcs.findAt(*points)
wallSet = pTank.Set(name='walls', faces=faces)
pTank.SectionAssignment(region=wallSet, sectionName='Section-wall')
faces = fcs.findAt(((0.0, 0.0, 0.0),),((0.0, Hei, 0.0),))
covSet = pTank.Set(name='covers', faces=faces)
pTank.SectionAssignment(region=covSet, sectionName='Section-cov')
#Assembly
root = md.rootAssembly
inst = root.Instance(name='tank', part=pTank, dependent=ON)
root.rotate(instanceList=('tank', ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(10.0, 0.0, 0.0), angle=90.0)
#step and Load-BC
md.BuckleStep(name='Buck', previous='Initial', numEigen=4, vectors=8,
    maxIterations=50)
points = []
for zi in Prib:
    points.append(((-Dwall/2.0, 0.0, zi),))
    points.append(((-Dwall/2.0, 0.0, zi-offSet),))

points.append(((-Dwall/2.0, 0.0, Hei-offSet),))
fcs = inst.faces
faces1 = fcs.findAt(*points)
hydroSur = root.Surface(name='hydroSur', side1Faces=faces1)
faces2 = fcs.findAt(((0.0, 0.0, 0.0),),)
fixSet = root.Set(name='fix', faces=faces2)
md.EncastreBC(name='fix', createStepName='Buck', region=fixSet)
md.Pressure(name='Hydro', createStepName='Buck', region=hydroSur, 
    distributionType=HYDROSTATIC, field='', magnitude=Press, 
    amplitude=UNSET, hZero=Hei, hReference=0.0)
#Mesh
pTank.seedPart(size=100.0, deviationFactor=0.1)
elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=S3, elemLibrary=STANDARD)
faces = pTank.faces
AllFace = pTank.Set(name='AllFace', faces=faces)
pTank.setElementType(regions=AllFace, elemTypes=(elemType1, elemType2))
pTank.generateMesh()
root.regenerate()
#Job and sumbit
job = mdb.Job(name=inpName, model='Model-1', numCpus=2, numDomains=2)
job.submit(consistencyChecking=OFF)
job.waitForCompletion()
odb = session.openOdb(name=inpName+'.odb')
step = odb.steps.values()[0]
Descr = step.frames[1].description
Result = float(re.split('= ', Descr)[-1])