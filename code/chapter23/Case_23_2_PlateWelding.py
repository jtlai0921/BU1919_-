# -*- coding: mbcs -*-
from math import *
from sys import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
import re, platform

def buildFor(Q=3000.0,factor1=1.0,source_a1=1.9,source_b1=3.2,
		source_c1=2.8,source_a2=1.9, weldingV=4.0,
        source_x0=0.0,source_y0=4.0,source_z0=0.0):
        
    tempName='dual_ellipse_plate.template'
    forName='dual_ellipse_Welding.for'
    f1=open(tempName,'r')
    f2=open(forName,'w')

    for line in f1.readlines():
        ss=line.strip()
        ss0=re.split('=',ss)
        ss1=re.split('=',line)
        if ss0[0]=='q':
            sstemp=ss1[0]+'='+str(Q)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='f1':
            sstemp=ss1[0]+'='+str(factor1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='a':
            sstemp=ss1[0]+'='+str(source_a1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='b':
            sstemp=ss1[0]+'='+str(source_b1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='c':
            sstemp=ss1[0]+'='+str(source_c1)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='aa':
            sstemp=ss1[0]+'='+str(source_a2)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='x0':
            sstemp=ss1[0]+'='+str(source_x0)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='y0':
            sstemp=ss1[0]+'='+str(source_y0)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='z0':
            sstemp=ss1[0]+'='+str(source_z0)+'\n'
            f2.writelines(sstemp)
        elif ss0[0]=='v':
            sstemp=ss1[0]+'='+str(weldingV)+'\n'
            f2.writelines(sstemp)
        else:
            f2.writelines(line)
    f1.close()
    f2.close()

    return forName
##========================================================
Temp0 = [0.0, 200.0, 400.0, 600.0, 800.0, 1000.0, 1200.0, 1400.0]#[oC]
fa = lambda T: 450+0.28*T-2.91e-4*T**2+1.34e-7*T**3#[J/kg/K]
Cp = [fa(item)*1.0e6 for item in Temp0]#[mJ/ton/K]
lma = lambda T:14.6+1.27e-2*T#[W/m/K]
Cd = [lma(item) for item in Temp0]#[mW/mm/K]
dens=((7.86e-9, ), )
specificheat=(zip(Cp, Temp0))
conductivity=(zip(Cd, Temp0))

L_p=100.0#mm
d_p=8.0#mm
w_p=50.0#mm
a_f=2.0#mm
theta=75.0
R_f=d_p*4.0#mm
partNum=50
timeoutputRelease=60.0
numoutputRelease=10
absZero=-273.15
boltZmann=5.67E-09#mW/mm2/K4
globalSize=8
upNum=4
dnNum=4
tkNum=8
myfilmCoeff=0.5#mW/mm2/oC
mysinkTemperature=20.0
myambientTemperature=20.0
myemissivity=0.4
initialTemp=20.0

weldingV=1.5#mm/s
s_Q=2000000.0#mW
s_a1=7.0#mm
s_b1=8.0#mm
s_c1=4.0#mm
s_a2=12.0#mm
s_x0=0.0#mm
s_y0=d_p/2.0#mm
s_z0=-4.0#mm
        
moveTime=L_p/partNum/weldingV
b_f=a_f+2.0*d_p/tan(theta/180.0*pi)
fc_y=d_p/2.0-sqrt(R_f**2-(b_f/2.0)**2)

weldModel = Mdb().models['Model-1']
#**********************Part definition********************************
sLef = weldModel.ConstrainedSketch(name='leftPlate', sheetSize=200.0)
sLef.Line(point1=(-w_p, d_p/2.0), point2=(-b_f/2.0, d_p/2.0))
sLef.Line(point1=(-b_f/2.0, d_p/2.0), point2=(-a_f/2.0, -d_p/2.0))
sLef.Line(point1=(-a_f/2.0, -d_p/2.0), point2=(-w_p, -d_p/2.0))
sLef.Line(point1=(-w_p, -d_p/2.0), point2=(-w_p, d_p/2.0))
pLef = weldModel.Part(name='PartLeft', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
pLef.BaseSolidExtrude(sketch=sLef, depth=L_p)

sRig = weldModel.ConstrainedSketch(name='RightPlate', sheetSize=200.0)
sRig.Line(point1=(b_f/2.0, d_p/2.0), point2=(w_p, d_p/2.0))
sRig.Line(point1=(w_p, d_p/2.0), point2=(w_p, -d_p/2.0))
sRig.Line(point1=(w_p, -d_p/2.0), point2=(a_f/2.0, -d_p/2.0))
sRig.Line(point1=(a_f/2.0, -d_p/2.0), point2=(b_f/2.0, d_p/2.0))
pRig = weldModel.Part(name='PartRight', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
pRig.BaseSolidExtrude(sketch=sRig, depth=L_p)

sFil = weldModel.ConstrainedSketch(name='Filler', sheetSize=200.0)
sFil.Line(point1=(-b_f/2.0, d_p/2.0), point2=(-a_f/2.0, -d_p/2.0))
sFil.Line(point1=(-a_f/2.0, -d_p/2.0), point2=(a_f/2.0, -d_p/2.0))
sFil.Line(point1=(a_f/2.0, -d_p/2.0), point2=(b_f/2.0, d_p/2.0))
sFil.ArcByCenterEnds(center=(0.0, fc_y), point1=(-b_f/2.0, d_p/2.0), 
    point2=(b_f/2.0, d_p/2.0),direction=CLOCKWISE)
pFil = weldModel.Part(name='PartFiller', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
pFil.BaseSolidExtrude(sketch=sFil, depth=L_p)
pFil = weldModel.parts['PartFiller']

#************************materials definition**************************
weldMat = weldModel.Material(name='mat')
weldMat.Density(table=dens)
weldMat.SpecificHeat(temperatureDependency=ON, table=specificheat)
weldMat.Conductivity(temperatureDependency=ON, table=conductivity)
weldModel.HomogeneousSolidSection(name='weld', material='mat')

set = pLef.Set(name = 'Lef', cells=pLef.cells)
pLef.SectionAssignment(region=set, sectionName='weld')
set = pRig.Set(name = 'Lef', cells=pRig.cells)
pRig.SectionAssignment(region=set, sectionName='weld')
set = pFil.Set(name = 'Lef', cells=pFil.cells)
pFil.SectionAssignment(region=set, sectionName='weld')

#************************Assembly ************************************
root = weldModel.rootAssembly
inst1 = root.Instance(name='PartFiller', part=pLef, dependent=ON)
inst2 = root.Instance(name='PartLeft', part=pRig, dependent=ON)
inst3 = root.Instance(name='PartRight', part=pFil, dependent=ON)
root.InstanceFromBooleanMerge(name='WeldingPart', instances=((inst1,
    inst2, inst3)), keepIntersections=ON, originalInstances=SUPPRESS, 
    domain=GEOMETRY)
#******************heat transfer boundary****************************
pWeld = weldModel.parts['WeldingPart']
datumYZ=pWeld.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, 
    offset=0.0)
xpart1=(-w_p-b_f/2.0)/2.0
xpart2=0.0
xpart3=(w_p+b_f/2.0)/2.0
for ii in range(partNum-1):
    zpart=L_p/partNum*(ii+1.0)
    ypart=0.0
    dp1=pWeld.DatumPointByCoordinate((0,-d_p,zpart))
    dp2=pWeld.DatumPointByCoordinate((-w_p,d_p,zpart))
    dp3=pWeld.DatumPointByCoordinate((w_p,d_p,zpart))
    dats=pWeld.datums
    dplane=pWeld.DatumPlaneByThreePoints(point1=dats[dp1.id],
        point2=dats[dp2.id], point3=dats[dp3.id])
    c4Part=pWeld.cells.findAt(((xpart1, ypart, zpart),),
        ((xpart2, ypart, zpart),), ((xpart3, ypart, zpart),),)
    pWeld.PartitionCellByDatumPlane(cells=c4Part,
        datumPlane=dats[dplane.id])

pkCells = pWeld.cells.getByBoundingBox(xMin=xpart1,xMax=xpart3,
    yMin=-d_p,yMax=2.0*d_p,zMin=-L_p,zMax=2.0*L_p)
dats = pWeld.datums
pWeld.PartitionCellByDatumPlane(datumPlane=dats[datumYZ.id], 
    cells=pkCells)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
face_p1_Yup=[]
face_p1_Ydn=[]
face_p2_Yup=[]
face_p2_Ydn=[]
face_p3_Yup=[]
face_p3_Ydn=[]
face_p4_Yup=[]
face_p4_Ydn=[]
face_p1_XY=[]
face_p2_XY=[]
face_p3_XY=[]
face_p4_XY=[]
face_bead_front_p2=[]
face_bead_front_p3=[]
face_bead_begin=[]
cell_p2=[]
cell_p3=[]
cell_bead=[]
faceZ=[]
edgeZ=[]
R_semi_filler=fc_y+R_f*cos(asin(b_f/2.0/R_f)/2.0)
xface_out_filler2=-R_f*sin(asin(b_f/2.0/R_f)/2.0)
xface_out_filler3=R_f*sin(asin(b_f/2.0/R_f)/2.0)

xcell_c1=(-w_p-b_f/2.0)/2.0
xcell_c2=-a_f/4.0
xcell_c3=a_f/4.0
xcell_c4=(w_p+b_f/2.0)/2.0
xface_c1=-w_p
xface_c2=-1.0*(a_f+b_f)/4.0
xface_c4=w_p
xface_c3=(a_f+b_f)/4.0
yface_up=d_p/2.0
yface_dn=-d_p/2.0
yface_fillerup=R_semi_filler
ycell=0.0
root = weldModel.rootAssembly
iWeld = root.instances['WeldingPart-1']
selectC=iWeld.cells
selectF=iWeld.faces

for jj in range(partNum):
    zCell=L_p/partNum*(jj+0.5)
    zFace=L_p/partNum*(jj+1.0)
    #Determine coord for selecting corresponding entities.
    face_p1_Yup.append(selectF.findAt(((xcell_c1,yface_up,zCell),)))
    face_p1_Ydn.append(selectF.findAt(((xcell_c1,yface_dn,zCell),)))
    face_p2_Yup.append(selectF.findAt(((xface_out_filler2,
        yface_fillerup,zCell),)))
    face_p2_Ydn.append(selectF.findAt(((xcell_c2,yface_dn,zCell),)))
    face_p3_Yup.append(selectF.findAt(((xface_out_filler3,
        yface_fillerup,zCell),)))
    face_p3_Ydn.append(selectF.findAt(((xcell_c3,yface_dn,zCell),)))
    face_p4_Yup.append(selectF.findAt(((xcell_c4,yface_up,zCell),)))
    face_p4_Ydn.append(selectF.findAt(((xcell_c4,yface_dn,zCell),)))
    #
    face_p1_XY.append(selectF.findAt(((xface_c1,ycell,zCell),)))
    face_p2_XY.append(selectF.findAt(((xface_c2,ycell,zCell),)))
    face_p3_XY.append(selectF.findAt(((xface_c3,ycell,zCell),)))
    face_p4_XY.append(selectF.findAt(((xface_c4,ycell,zCell),)))
    #
    face_bead_front_p2.append(selectF.findAt(((xcell_c2,ycell,zFace),)))
    face_bead_front_p3.append(selectF.findAt(((xcell_c3,ycell,zFace),)))
    #
    cell_p2.append(selectC.findAt(((xcell_c2,ycell,zCell),)))
    cell_p3.append(selectC.findAt(((xcell_c3,ycell,zCell),)))
    cell_bead.append(selectC.findAt(((xcell_c2,ycell,zCell),)))
    cell_bead.append(selectC.findAt(((xcell_c3,ycell,zCell),)))
    edgeZ.extend([((-w_p, d_p/2.0, zCell),),((w_p, d_p/2.0, zCell),),
        ((-w_p, -d_p/2.0, zCell),),((w_p, -d_p/2.0, zCell),),
        ((-b_f/2.0, d_p/2.0, zCell),),((b_f/2.0, d_p/2.0, zCell),),
        ((-a_f/2.0, -d_p/2.0, zCell),),((a_f/2.0, -d_p/2.0, zCell),),
        ((0.0, fc_y+R_f, zCell),),((0.0, -d_p/2.0, zCell),)])

face_bead_begin.append(selectF.findAt(((xcell_c2,ycell,0.0),)))
face_bead_begin.append(selectF.findAt(((xcell_c3,ycell,0.0),)))

faceZ.append(selectF.findAt(((xcell_c1,ycell,0.0),)))
faceZ.append(selectF.findAt(((xcell_c4,ycell,0.0),)))
faceZ.append(selectF.findAt(((xcell_c1,ycell,L_p),)))
faceZ.append(selectF.findAt(((xcell_c4,ycell,L_p),)))
#****************************STEP Settings*************************
restsurfaceName='Surface-rest'
allsetName='Set-all'
beadsetName='Set-allfiller'
sidesurfaceName='Surface-side'
allset=root.Set(cells=iWeld.cells, name=allsetName)
rests=face_p1_XY+face_p4_XY+face_p1_Yup+face_p1_Ydn+face_p4_Yup\
    +face_p4_Ydn+faceZ
restsurface=root.Surface(side1Faces=rests, name=restsurfaceName)
beadset=root.Set(cells=cell_bead,name=beadsetName)
sidesurface=root.Surface(side2Faces=face_p3_XY+face_p2_XY, 
    name=sidesurfaceName)
weldModel.HeatTransferStep(name='Step-t0', previous='Initial', 
    timePeriod=1e-08, maxNumInc=10000, initialInc=1e-08, minInc=1e-13, 
    maxInc=1e-8, deltmx=200.0)
fOR = weldModel.fieldOutputRequests['F-Output-1']
fOR.setValues(frequency=LAST_INCREMENT, variables=('HFL', 'NT'))
#***********Boundary condition for the initial step-t0********************
weldModel.FilmCondition(name='film', createStepName='Step-t0', 
    surface=restsurface, definition=EMBEDDED_COEFF, filmCoeff=myfilmCoeff, 
    sinkTemperature=mysinkTemperature)
weldModel.RadiationToAmbient(name='radiation', createStepName='Step-t0',
    surface=restsurface, radiationType=AMBIENT, distributionType=UNIFORM,
    emissivity=myemissivity, ambientTemperature=myambientTemperature)
weldModel.BodyHeatFlux(name='bodyFlux', createStepName='Step-t0', 
    region=allset, magnitude=1.0, distributionType=USER_DEFINED)
weldModel.ModelChange(name='deactivate_all', createStepName='Step-t0',
    region=beadset, activeInStep=False, includeStrain=False)
weldModel.Temperature(name='Predefined', createStepName='Initial', 
    region=allset, magnitudes=(initialTemp,))
weldModel.FilmCondition(name='film_surface_all_t0', 
    createStepName='Step-t0', surface=sidesurface, 
    definition=EMBEDDED_COEFF, filmCoeff=myfilmCoeff, 
    sinkTemperature=mysinkTemperature)
weldModel.RadiationToAmbient(name='radiation_surface_all_t0', 
    createStepName='Step-t0',surface=sidesurface, radiationType=AMBIENT,
    distributionType=UNIFORM, emissivity=myemissivity, 
    ambientTemperature=myambientTemperature)
#***********Boundary condition for the following steps********************
stepNum=partNum
preStep='Step-t0'
preRadiationBC='radiation_surface_all_t0'
preFilmBC='film_surface_all_t0'
preFoutput='F-Output-1'
for i in range(stepNum):
    stepNamechange='step-t'+str(i+1)
    stepNameheat  ='step-'+str(i+1)
    sidesurface   ='surfaceside_t'+str(i+1)
    setActivate   ='setActivate_t'+str(i+1)
    film_surface_all='film_surface_all_t'+str(i+1)
    radiation_surface_all='radiation_surface_all_t'+str(i+1)
    FoutputName ='F-Output-step'+str(i+1)
    ##############setting for step_t
    weldModel.HeatTransferStep(name=stepNameheat, previous=preStep, 
        timePeriod=moveTime, maxNumInc=10000, initialInc=moveTime*0.005, 
        minInc=moveTime*1e-8, maxInc=moveTime*0.03, deltmx=200.0)
    weldModel.FieldOutputRequest(name=FoutputName,numIntervals=1,
        createStepName=stepNameheat, variables=('HFL', 'NT'))
    ##############set and surface for step_t
    eleSet=cell_p2[i:i+1]+cell_p3[i:i+1]
    activeSet=root.Set(cells=eleSet, name=setActivate)
    sur_side1=[]
    sur_side2=[]
    if i!=(stepNum-1):
        sur_side1=face_p3_Ydn[0:i+1]+face_p3_Yup[0:i+1]+\
            face_p2_Ydn[0:i+1]+face_p2_Yup[0:i+1]
        sur_side2=face_p2_XY[i+1:]+face_bead_front_p2[i:i+1]+\
            face_bead_front_p3[i:i+1]+face_p3_XY[i+1:]
    else:
        sur_side1=face_p3_Ydn[0:i+1]+face_p3_Yup[0:i+1]+\
            face_p2_Ydn[0:i+1]+face_p2_Yup[0:i+1]+\
            face_bead_front_p3[i:i+1]+face_bead_front_p2[i:i+1]
        sur_side2=face_p2_XY[i+1:]+face_p3_XY[i+1:]
    sur_all=root.Surface(side1Faces=sur_side1,side2Faces=sur_side2, 
        name=sidesurface)  
    ############## BC for step_t
    weldModel.ModelChange(name=setActivate, 
        createStepName=stepNameheat, region=activeSet, 
        activeInStep=True, includeStrain=False)
    weldModel.FilmCondition(name=film_surface_all, 
        createStepName=stepNameheat, surface=sur_all, 
        definition=EMBEDDED_COEFF, filmCoeff=myfilmCoeff,
        sinkTemperature=mysinkTemperature)
    weldModel.RadiationToAmbient(name=radiation_surface_all, 
        createStepName=stepNameheat, surface=sur_all, 
        radiationType=AMBIENT, distributionType=UNIFORM, 
        emissivity=myemissivity, ambientTemperature=myambientTemperature)  
    ############## deativate BC for step_t
    weldModel.interactions[preRadiationBC].deactivate(stepNameheat)
    weldModel.interactions[preFilmBC].deactivate(stepNameheat)
    ############## update the temp variables for step_t
    preStep=stepNameheat
    preRadiationBC=film_surface_all
    preFilmBC=radiation_surface_all
    preFoutput=FoutputName

lastStep='step-t'+str(stepNum)
film_bead_end='film_bead_begining_t1'
radi_bead_end='radi_bead_begining_t1'
bead_end_surface='bead_begining'
sur_side1=face_bead_begin
beginsurface=root.Surface(side1Faces=sur_side1, name=bead_end_surface)    
weldModel.FilmCondition(name=film_bead_end, createStepName='step-1', 
    surface=beginsurface, definition=EMBEDDED_COEFF, filmCoeff=myfilmCoeff, 
    sinkTemperature=mysinkTemperature)
weldModel.RadiationToAmbient(name=radi_bead_end, createStepName='step-1',
    surface=beginsurface, radiationType=AMBIENT, distributionType=UNIFORM,
    emissivity=myemissivity, ambientTemperature=myambientTemperature)
##############step for step_release
releaseName='stepRelease'
weldModel.HeatTransferStep(name=releaseName, previous=preStep, 
    timePeriod=timeoutputRelease, maxNumInc=10000, 
    initialInc=moveTime*0.005, minInc=1e-8*timeoutputRelease, 
    maxInc=moveTime*0.2, deltmx=200.0)
weldModel.FieldOutputRequest(name='release_output',createStepName=\
    releaseName, numIntervals=numoutputRelease)
weldModel.loads['bodyFlux'].deactivate('stepRelease')
weldModel.setValues(absoluteZero=absZero, stefanBoltzmann=boltZmann)

#****************************Mesh the part****************************
pWeld.setMeshControls(regions=pWeld.cells, technique=STRUCTURED)
pWeld.seedPart(size=globalSize, deviationFactor=0.1)
xfindedge_p1=(-w_p-b_f/2.0)/2.0
xfindedge_p2=a_f/4.0
xfindedge_p4=(w_p+b_f/2.0)/2.0
yfindedge_arc=fc_y+R_f*cos(asin(b_f/2.0/R_f)/2.0)
xfindedge_arc=R_f*sin(asin(b_f/2.0/R_f)/2.0)
xfindedge_g2=(a_f/2.0+b_f/2.0)/2.0
alledges = pWeld.edges
pkE3=alledges.findAt(((xfindedge_arc,yfindedge_arc,0.0),),
    ((-xfindedge_arc,yfindedge_arc,0.0),))
pkE4=alledges.findAt(((xfindedge_p2,-d_p/2.0,0.0),),
    ((-xfindedge_p2,-d_p/2.0,0.0),))
pkE5=alledges.findAt(((-w_p,0.0,0.0),),((-xfindedge_g2,0.0,0.0),),
    ((0.0,0.0,0.0),),((xfindedge_g2,0.0,0.0),),((w_p,0.0,0.0),),)
pkE6 = alledges.findAt(*edgeZ)
pWeld.seedEdgeByNumber(edges=pkE3, number=upNum, constraint=FIXED)
pWeld.seedEdgeByNumber(edges=pkE4, number=dnNum, constraint=FIXED)
pWeld.seedEdgeByNumber(edges=pkE5, number=tkNum, constraint=FIXED)
LNum = int(L_p/partNum/(d_p/tkNum))
pWeld.seedEdgeByNumber(edges=pkE6, number=LNum, constraint=FIXED)
if (d_p/tkNum)<globalSize*0.8:
    minSize=d_p/tkNum
else:
    minSize=globalSize*0.5

for jj in range(partNum+1):
    zEdge=L_p/partNum*jj
    #Determine the coord for select corresponding entities.
    pickedEdges11=alledges.findAt(((xfindedge_p1,d_p/2.0,zEdge),))
    pickedEdges12=alledges.findAt(((xfindedge_p1,-d_p/2.0,zEdge),))
    pickedEdges21=alledges.findAt(((xfindedge_p4,d_p/2.0,zEdge),))
    pickedEdges22=alledges.findAt(((xfindedge_p4,-d_p/2.0,zEdge),))
    pWeld.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges11, 
        minSize=minSize, maxSize=globalSize, constraint=FINER)
    pWeld.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges12, 
        minSize=minSize, maxSize=globalSize, constraint=FINER)
    pWeld.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges21, 
        minSize=minSize, maxSize=globalSize, constraint=FINER)
    pWeld.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges22, 
        minSize=minSize, maxSize=globalSize, constraint=FINER)

elemType1 = mesh.ElemType(elemCode=DC3D8)
elemType2 = mesh.ElemType(elemCode=DC3D6)
elemType3 = mesh.ElemType(elemCode=DC3D4)
eTypes = (elemType1, elemType2, elemType3)
pkCells =(pWeld.cells, )
pWeld.setElementType(regions=pkCells, elemTypes=eTypes)
pWeld.generateMesh()
root.regenerate()

#*************Create the inp file and submit the job********************
jobName='Welding_plate'
dfluxName=buildFor(Q=s_Q,factor1=1.0,source_a1=s_a1,source_b1=s_b1,
    source_c1=s_c1,source_a2=s_a2, weldingV=weldingV,
    source_x0=s_x0,source_y0=s_y0,source_z0=s_z0)
mdb.Job(name=jobName, model='Model-1', userSubroutine=dfluxName, 
    multiprocessingMode=DEFAULT, numCpus=8, numDomains=8)
#mdb.jobs[jobName].writeInput()