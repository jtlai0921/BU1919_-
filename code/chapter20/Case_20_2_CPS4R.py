# -*- coding: mbcs -*-
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
###################parameters#################################
L = 300.0
W = 300.0
R = 3.0
Press = 10.0
NumList = [2, 4, 8, 16, 32]
MkList = [HOLLOW_CIRCLE, HOLLOW_SQUARE, HOLLOW_DIAMOND, HOLLOW_TRI,
    CROSS, XMARKER, POINT]
curveList = []
Mdb()
vp = session.viewports['Viewport: 1']
for (i, NR) in enumerate(NumList):
    dR = R
    NumR = NR
    Size = 4.0
    NumdR = int(dR/(pi/4.0*R/NumR))
    ModelName = 'HolePlate'+str(i)
    INPName = 'HolePlate'+str(i)
    PNGName = 'CPS4R_'+str(NumR)+'Element'
    dataName = 'Num='+str(NumR*2)
    #constructe the sketch
    m = mdb.Model(name=ModelName)
    s = m.ConstrainedSketch(name='plate', sheetSize=200.0)
    g = s.geometry
    g1 = s.Line(point1=(0.0, 0.0), point2=(0.0, L/2.0))
    g2 = s.Line(point1=(0.0, L/2.0), point2=(W/2.0, L/2.0))
    g3 = s.Line(point1=(W/2.0, L/2.0), point2=(W/2.0, 0.0))
    g4 = s.Line(point1=(W/2.0, 0.0), point2=(0.0, 0.0))
    g5 = s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(R, 0.0))
    s.autoTrimCurve(curve1=g1, point1=(0.0, R/2.0))
    s.autoTrimCurve(curve1=g4, point1=(R/2.0, 0.0))
    s.autoTrimCurve(curve1=g5, point1=(-R, 0.0))
    p=m.Part(name='plate',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
    p.BaseShell(sketch=s)
    #build material model
    matSteel = m.Material(name='steel')
    matSteel.Elastic(table=((210000.0, 0.3), ))
    m.HomogeneousSolidSection(name='Section-steel', 
        material='steel', thickness=0.1)
    fplate = p.faces
    plate = p.Set(name='plate', faces=fplate)
    p.SectionAssignment(region=plate, sectionName='Section-steel',
        offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    #Assembly
    a = m.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    inst = a.Instance(name='plate-1', part=p, dependent=ON)
    ePlate = inst.edges
    edges1 = ePlate.findAt(((0.0, (R+L/2.0)/2.0, 0.0),),)
    XsymmSet = a.Set(edges=edges1, name='Xsymm')
    edges2 = ePlate.findAt((((R+W/2.0)/2., 0.0, 0.0),),)
    YsymmSet = a.Set(edges=edges2, name='Ysymm')
    side1Edges1 = ePlate.findAt((((R+W/2.0)/2., L/2.0, 0.0),),)
    Psurface = a.Surface(side1Edges=side1Edges1, name='Surf-P')
    #Load step and boundary
    m.StaticStep(name='Load', previous='Initial')
    m.XsymmBC(name='BC-Xsymm', createStepName='Initial', region=XsymmSet)
    m.YsymmBC(name='BC-Ysymm', createStepName='Initial', region=YsymmSet)
    m.Pressure(name='Pressure', createStepName='Load', magnitude=-Press,
        region=Psurface)
    #Generate Mesh
    f0, d0 = p.faces, p.datums
    pd1 = p.DatumPointByCoordinate(coords=(0.0, 0.0, 0.0))
    pd2 = p.DatumPointByCoordinate(coords=(0.0, R+dR, 0.0))
    pd3 = p.DatumPointByCoordinate(coords=(R+dR, 0.0, 0.0))
    pd4 = p.DatumPointByCoordinate(coords=(R+dR, R+dR, 0.0))
    pd5 = p.DatumPointByCoordinate(coords=(R+dR, R+dR, 10.0))
    d2 = p.datums
    plane1 = p.DatumPlaneByThreePoints(point1=d0[pd1.id], 
        point2=d0[pd4.id], point3=d0[pd5.id])
    plane2 = p.DatumPlaneByThreePoints(point1=d0[pd2.id], 
        point2=d0[pd4.id], point3=d0[pd5.id])
    plane3 = p.DatumPlaneByThreePoints(point1=d0[pd3.id], 
        point2=d0[pd4.id], point3=d0[pd5.id])
    p.PartitionFaceByDatumPlane(datumPlane=d0[plane1.id], faces=f0)
    f1 = p.faces
    p.PartitionFaceByDatumPlane(datumPlane=d0[plane2.id], faces=f1)
    f2 = p.faces
    p.PartitionFaceByDatumPlane(datumPlane=d0[plane3.id], faces=f2)
    e2 = p.edges
    temp = R+dR/2.0
    pickedEdges1 = e2.findAt(((temp, 0.0, 0.0),), ((0.0, temp, 0.0),), 
        ((temp*0.707, temp*0.707, 0.0),), )
    p.seedEdgeByNumber(edges=pickedEdges1, number=NumdR, constraint=FIXED)
    pickedEdges2 = e2.findAt(((R*cos(pi/3), R*sin(pi/3), 0.0),), 
        ((R*cos(pi/6), R*sin(pi/6), 0.0),), (((R+dR)/2.0, R+dR, 0.0),), 
        ((R+dR, (R+dR)/2.0, 0.0),),)
    p.seedEdgeByNumber(edges=pickedEdges2, number=NumR, constraint=FIXED)
    p.seedPart(size=Size, deviationFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=CPS4R, secondOrderAccuracy=OFF)
    elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)
    p.setElementType(regions=plate, elemTypes=(elemType1, elemType2))
    f3 = p.faces
    p.setMeshControls(regions=f3, technique=FREE, algorithm=MEDIAL_AXIS)
    f4 = f3.findAt(((temp*cos(pi/6), temp*sin(pi/6), 0.0),), 
        ((temp*cos(pi/3), temp*sin(pi/3), 0.0),))
    p.setMeshControls(regions=f4, technique=STRUCTURED, elemShape=QUAD)
    p.generateMesh()
    a.regenerate()
    #Create Job
    mdb.Job(name=INPName, model=ModelName, numCpus=1)
    mdb.jobs[INPName].submit(consistencyChecking=OFF)
    mdb.jobs[INPName].waitForCompletion()
    #Print the result and extract the data
    odb = session.openOdb(name=INPName+'.odb')
    vp.setValues(displayedObject=odb)
    pth = session.Path(name='Hole', type=CIRCUMFERENTIAL, expression=
        ((0, 0, 10), (0, 0, -10), (0, R, 0)), circleDefinition=ORIGIN_AXIS,
        numSegments=16, startAngle=0, endAngle=90, radius=CIRCLE_RADIUS)
    CC = odb.rootAssembly.DatumCsysByThreePoints(name='CC', origin=(0,0,0),
        point1=(0,1,0),point2=(1,0,0),coordSysType=CYLINDRICAL)
    vp.odbDisplay.basicOptions.setValues(transformationType=USER_SPECIFIED, 
        datumCsys=CC)
    vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
    vp.odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=
        INTEGRATION_POINT, refinement=(COMPONENT, 'S22'), )
    vp.odbDisplay.commonOptions.setValues(visibleEdges=FREE)
    vp.odbDisplay.contourOptions.setValues(spectrum='White to black')
    vp.restore()
    vp.setValues(width=80,height=80)
    vp.view.fitView()
    vp.viewportAnnotationOptions.setValues(state=OFF, annotations=OFF, 
        compass=OFF, legendBox=OFF, legendTitle=OFF, legendDecimalPlaces=1,
        legendNumberFormat=FIXED)
    session.printOptions.setValues(rendition=GREYSCALE, vpDecorations=OFF, 
        reduceColors=False)
    session.printToFile(fileName=PNGName, format=PNG, canvasObjects=(vp,))
    data = session.XYDataFromPath(name=dataName, path=pth, shape=UNDEFORMED,
        includeIntersections= False, labelType=TRUE_DISTANCE)
    sCurve = session.Curve(xyData=data)
    sCurve.setValues(displayTypes=(SYMBOL,), legendLabel=dataName, 
        useDefault=OFF)
    sCurve.symbolStyle.setValues(marker=MkList[i],size=2.0,color='Black')
    curveList.append(sCurve)
#=========================generate the theory data to plot==================
angles = [pi/2.0/16.0*i for i in range(0,17,1)]
xData = [R*a for a in angles]
yData = [Press/2.0*(2.0-4.0*cos(2.0*a)) for a in angles]
theoData = zip(xData,yData)
xQuantity = visualization.QuantityType(type=PATH)
yQuantity = visualization.QuantityType(type=STRESS)
theoData = session.XYData(data=theoData,name='Theory',legendLabel='Theory',
    axis1QuantityType=xQuantity, axis2QuantityType=yQuantity)
theoCurve = session.Curve(xyData=theoData)
theoCurve.setValues(displayTypes=(SYMBOL,), legendLabel='Theory', 
    useDefault=OFF)
theoCurve.symbolStyle.setValues(marker=MkList[len(NumList)+1],size=2.0,
    color='Black')
curveList.append(theoCurve)
#============================generate picture===============================
phPlot = session.XYPlot(name='plate-hole-element-number')
phPlot.title.setValues(text='Result of different element number: CPS4R')
chartName = phPlot.charts.keys()[0]
chart = phPlot.charts[chartName]
chart.setValues(curvesToPlot=curveList, )
chart.gridArea.style.setValues(color='White')
chart.legend.area.style.setValues(color='Gray')
phPlot.title.style.setValues(
    font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
chart.legend.textStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-180-*-*-p-*-*-*')
chart.legend.titleStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-180-*-*-p-*-*-*')
chart.axes1[0].labelStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
chart.axes1[0].titleStyle.setValues(
    font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
chart.axes2[0].labelStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
chart.axes2[0].titleStyle.setValues(
    font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
vp.setValues(width=180,height=150,origin=(0,-20))
vp.setValues(displayedObject=phPlot)
session.printToFile(fileName='CPS4R_Result', format=PNG, 
    canvasObjects=( vp, ))