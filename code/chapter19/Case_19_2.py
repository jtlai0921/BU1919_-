# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
from math import *
from odbAccess import *

wireR=1.0#
SpringR=15.0#
NN=8
GapR=0.3
angle=5.0#degree
Spitch=wireR*(2.0+GapR)/cos(angle/180.0*pi)#
DR=wireR+SpringR
RatioRr=SpringR/wireR
ur2 = pi

inpName='SoildSpring_Rr'+str(int(RatioRr))
Mdb()
TheModel = mdb.models['Model-1']
s = TheModel .ConstrainedSketch(name='springSection', 
    sheetSize=200.0)
s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.CircleByCenterPerimeter(center=(DR, 0.0), point1=(DR+wireR, 0.0))
p = TheModel .Part(name='spring', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p.BaseSolidRevolve(sketch=s, angle=360.0*(NN+1), flipRevolveDirection=OFF, 
    pitch=Spitch, flipPitchDirection=OFF, moveSketchNormalToPath=ON)
TheMaterial = TheModel .Material(name='steel')
TheMaterial.Elastic(table=((210000.0, 0.3), ))
TheModel .HomogeneousSolidSection(name='SteelSection', 
    material='steel', thickness=None)
c = p.cells
secSet = p.Set(name='secSet', cells=c)
p.SectionAssignment(region=secSet, sectionName='SteelSection', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

a = TheModel .rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name='spring-1', part=p, dependent=ON)
p1=a.ReferencePoint(point=(0.0,0.0,0.0))
p2=a.ReferencePoint(point=(0.0,-1.0*(NN+1)*Spitch,0.0))

xx1=SpringR*cos(0.5*pi)
zz1=SpringR*sin(0.5*pi)
yy1=-0.25*Spitch
xx2=SpringR*cos((NN+0.75)*2.0*pi)
zz2=SpringR*sin((NN+0.75)*2.0*pi)
yy2=-1.0*(NN+0.75)*Spitch
f = a.instances['spring-1'].faces
faces1 = f.findAt(((xx2, yy2, zz2),),)
Setfix=a.Set(faces=faces1, name='Set-fix')
faces1 = f.findAt(((xx1, yy1, zz1),),)
Settwist=a.Set(faces=faces1, name='Set-twist')
r1 = a.referencePoints
SetfixRP=a.Set(referencePoints=(r1[p2.id],), name='Set-fixRP')
SettwistRP=a.Set(referencePoints=(r1[p1.id],), name='Set-twistRP')

TheModel .StaticStep(name='Step-twist', previous='Initial',
    initialInc=0.05, minInc=1e-06, maxInc=0.2, maxNumInc=1000, nlgeom=ON)
TheModel .fieldOutputRequests['F-Output-1'].setValues(variables=
    ('S', 'LE', 'U', 'RF', 'RM', 'CF'), numIntervals=10, timeMarks=OFF)
TheModel .Coupling(name='Constraint-fix', controlPoint=SetfixRP,
    surface=Setfix, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
    localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
TheModel .Coupling(name='Constraint-twist', controlPoint=SettwistRP, 
    surface=Settwist, influenceRadius=WHOLE_SURFACE,
    couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON,
    ur2=ON, ur3=ON)
TheModel .DisplacementBC(name='BC-fix', createStepName='Initial',
    region=SetfixRP, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
TheModel .DisplacementBC(name='BC-twist',
    createStepName='Initial', region=SettwistRP, u1=SET, u2=SET, u3=SET,
    ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM,
    fieldName='', localCsys=None)
TheModel .boundaryConditions['BC-twist'].setValuesInStep(stepName=
    'Step-twist', ur2=ur2)

c = p.cells
p.setMeshControls(regions=c, technique=SWEEP)
NSize=16
LSize=DR*pi*2/64
e = p.edges
NEdges, LEdges, CriL = [], [], 2.0*pi*wireR
for i in range(len(e)):
    if abs(e[i].getSize()-CriL)/CriL<0.02:
        NEdges.append(e[i])
    else:
        LEdges.append(e[i])
p.seedEdgeByNumber(edges=NEdges, number=NSize, constraint=FIXED)
p.seedEdgeBySize(edges=LEdges, size=LSize, deviationFactor=0.1,
    constraint=FINER)
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
p.setElementType(regions=(c,), elemTypes=(elemType1, 
    elemType2, elemType3))
p.generateMesh()
a.regenerate()

Npie = len(LEdges)
mdb.Job(name=inpName, model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=50, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs[inpName].submit(consistencyChecking=OFF)
mdb.jobs[inpName].waitForCompletion()
odbPath=inpName+'.odb'
odb = openOdb(odbPath)
nset = odb.rootAssembly.nodeSets['CONSTRAINT-TWIST_REFERNCE_POINT']
frame=odb.steps.values()[-1].frames[-1]
foutput=frame.fieldOutputs['RM']
fvalues=foutput.getSubset(region=nset).values[0].data[1]
odb.close()
print fvalues