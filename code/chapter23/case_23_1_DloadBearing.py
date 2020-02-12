# -*- coding: mbcs -*-
import math, os, os.path, re
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

Mdb()
Tforce=120000.0
rad1=80.0
rad0=8.0
omega=2.0*pi
temp1=0.0
CLen=1.0
E1=210000.0
E2=210000.0
v1=0.3
v2=0.3
num=12

wid1 = 20.0
wid2 = 20.0
imodel = mdb.models['Model-1']
s = imodel.ConstrainedSketch(name='out', sheetSize=200.0)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(rad1, 0.0))
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(rad1+wid1, 0.0))
pOut = imodel.Part(name='out', dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
pOut.BaseShell(sketch=s)
s = imodel.ConstrainedSketch(name='roller', sheetSize=200.0)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(rad0, 0.0))
pRoller = imodel.Part(name='roller', dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
pRoller.BaseShell(sketch=s)
s = imodel.ConstrainedSketch(name='in', sheetSize=200.0)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(rad1-rad0*2.0-wid2, 0.0))
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(rad1-rad0*2.0, 0.0))
pIn = imodel.Part(name='in', dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
pIn.BaseShell(sketch=s)

iMat = imodel.Material(name='steel')
iMat.Density(table=((7.86e-09, ), ))
iMat.Elastic(table=((E1, v1), ))
imodel.HomogeneousSolidSection(name='Sec', material='steel', thickness=CLen)
f = pOut.faces
pOutSet = pOut.Set(faces=f, name='pOutSet')
pOut.SectionAssignment(region=pOutSet, sectionName='Sec')
f = pRoller.faces
pRollerSet = pRoller.Set(faces=f, name='pRollerSet')
pRoller.SectionAssignment(region=pRollerSet, sectionName='Sec')
f = pIn.faces
pInSet = pIn.Set(faces=f, name='pIn')
pIn.SectionAssignment(region=pInSet, sectionName='Sec')

root = imodel.rootAssembly
root.DatumCsysByDefault(CARTESIAN)
iOut=root.Instance(name='out', part=pOut, dependent=ON)
iIn=root.Instance(name='in', part=pIn, dependent=ON)
rp0 = root.ReferencePoint(point=(0,0,0))
refPoints1=(root.referencePoints[rp0.id], )
rpInSet = root.Set(referencePoints=refPoints1, name='rpInSet')
iInfaces = iIn.faces
iInSet=root.Set(faces=iInfaces, name='iInSet')
imodel.RigidBody(name='Cons-1', refPointRegion=rpInSet, bodyRegion=iInSet)
rpRollers=[]
for i in range(num):
    name='Roller'+str(i+1)
    iRoller=root.Instance(name=name, part=pRoller, dependent=ON)
    posi = float(i)/num*2.0*math.pi
    RAD = rad1-rad0
    vector = (RAD*math.cos(posi), RAD*math.sin(posi), 0.0)
    iRoller.translate(vector=vector)
    rpRoller = root.ReferencePoint(point=vector)
    rfPoint = root.referencePoints[rpRoller.id]
    rpRollers.append(rfPoint)
    rpSet = root.Set(referencePoints=(rfPoint,), name='rpRoller'+str(i+1))
    faces = iRoller.faces
    iRollerSet=root.Set(faces=faces, name='iRollerSet'+str(i+1))
    imodel.Coupling(name='roller'+str(i+1), controlPoint=rpSet, 
        surface=iRollerSet, influenceRadius=WHOLE_SURFACE, 
        couplingType=KINEMATIC, u1=ON, u2=ON, ur3=OFF)

rp = root.ReferencePoint(point=(0,0,0))
refPoints=(root.referencePoints[rp.id], )
rpCenter = root.Set(referencePoints=refPoints, name='rpCenter')
rpRs = root.Set(referencePoints=rpRollers, name='rpRs')
imodel.Coupling(name='center', controlPoint=rpCenter, surface=rpRs, 
    influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
    u1=ON, u2=ON, ur3=OFF)
rpFix = root.ReferencePoint(point=(0,0,0))
refPoints=(root.referencePoints[rpFix.id], )
rpFix = root.Set(referencePoints=refPoints, name='rpFix')
es = iOut.edges
picked1 = es.findAt(((rad1,0,0),),)
picked2 = es.findAt(((rad1+wid1,0,0),),)
fixSet = root.Set(edges=picked2, name='fixOut')
imodel.Coupling(name='fixOut', controlPoint=rpFix, surface=fixSet, 
    influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
    u1=ON, u2=ON, ur3=ON)
pressSurf= root.Surface(side1Edges=picked1, name='PressSurf')
imodel.StaticStep(name='rolling', previous='Initial', 
    maxNumInc=10000, initialInc=0.01, minInc=1e-08, maxInc=0.01, nlgeom=ON)
pIn.seedPart(size=wid2/2.0)
pIn.generateMesh()
pRoller.seedPart(size=rad0/4.0)
pRoller.generateMesh()
pOut.seedPart(size=wid1/2.0)
es = pOut.edges
picked1 = es.findAt(((rad1,0,0),),)
picked2 = es.findAt(((rad1+wid1,0,0),),)
pOut.seedEdgeBySize(edges=picked1, size=0.2)
pOut.seedEdgeBySize(edges=picked2, size=wid1/2.0)
pOut.generateMesh()
imodel.DisplacementBC(name='BC-OutFix', createStepName='Initial', 
    region=rpFix, u1=SET, u2=SET, ur3=SET, distributionType=UNIFORM)
imodel.Pressure(name='Load-OutPress', createStepName='rolling', 
    region=pressSurf, distributionType=USER_DEFINED, magnitude=1.0)
BC_In = imodel.DisplacementBC(name='BC-InFix', createStepName='Initial', 
    region=rpInSet, u1=SET, u2=SET, ur3=SET, distributionType=UNIFORM)
BC_In.setValuesInStep(stepName='rolling', ur3=1.0*omega)
BC_Cent = imodel.DisplacementBC(name='BCCent', createStepName='Initial', 
    region=rpCenter, u1=SET, u2=SET, ur3=SET, distributionType=UNIFORM)
BC_Cent.setValuesInStep(stepName='rolling', 
    ur3=1.0*omega*(rad1-2.0*rad0)/rad1)
for i in range(num):
    set=root.sets['rpRoller'+str(i+1)]
    BC = imodel.DisplacementBC(name='BC'+str(i+1), createStepName='Initial', 
        region=set, u1=SET, u2=SET, ur3=SET, distributionType=UNIFORM)
    BC.setValuesInStep(stepName='rolling', ur3=-1.0*omega*(rad1-2.0*rad0)/rad0)
#build the Dload subroutine file for current case
DloadName = 'Bearing.for'
cwd = os.getcwd()
DloadTemplateName = 'DloadBearing.for'
DloadTemplate = os.path.join(cwd, DloadTemplateName)
DloadFile = os.path.join(cwd, DloadName)
f1=open(DloadTemplate,'r')
f2=open(DloadFile,'w')
for line in f1.readlines():
    ss=line.strip()
    ss0=re.split('=',ss)
    ss1=re.split('=',line)
    if len(ss0)==3:
        sstemp=ss1[0]+'='+ss1[1]+'='+str(num)+')\n'
        f2.writelines(sstemp)
    elif ss0[0]=='Tforce':
        sstemp=ss1[0]+'='+str(Tforce)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='rad1':
        sstemp=ss1[0]+'='+str(rad1)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='Dia0':
        sstemp=ss1[0]+'='+str(rad0*2.0)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='omega':
        sstemp=ss1[0]+'='+str(omega)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='CLen':
        sstemp=ss1[0]+'='+str(CLen)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='E1':
        sstemp=ss1[0]+'='+str(E1)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='E2':
        sstemp=ss1[0]+'='+str(E2)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='v1':
        sstemp=ss1[0]+'='+str(v1)+'\n'
        f2.writelines(sstemp)
    elif ss0[0]=='v2':
        sstemp=ss1[0]+'='+str(v2)+'\n'
        f2.writelines(sstemp)
    else:
        f2.writelines(line)
f1.close()
f2.close()
mdb.Job(name='Bearing12', model='Model-1', userSubroutine=DloadFile, 
    multiprocessingMode=DEFAULT, numCpus=8, numGPUs=0, numDomains=8)