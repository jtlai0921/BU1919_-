# -*- coding: mbcs -*-
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
###################parameters#################################
D = 100.0
d = 50.0
Ratio = 0.1
Press = 10
r = Ratio*d
H = 60.0
h = 60.0
NumList = [2, 4, 8, 16, 32]
MkList = [HOLLOW_CIRCLE, HOLLOW_SQUARE, HOLLOW_DIAMOND, HOLLOW_TRI,
    CROSS, XMARKER, POINT]
curveList = []
Mdb()
vp = session.viewports['Viewport: 1']
for (i, NR) in enumerate(NumList):
    dR = r
    dH = r
    NumR = NR
    Size = 2.0
    NumdR = int(dR/(pi/2.0*r/NumR))
    ModelName = 'TPart'+str(i)
    INPName = 'TPart'+str(i)
    PNGName = 'CPS4R_'+str(NumR)+'Element'
    dataName = 'Num='+str(NumR)
    #constructe the TPart sketch
    m = mdb.Model(name=ModelName)
    s = m.ConstrainedSketch(name='TPart', sheetSize=200.0)
    g = s.geometry
    g1 = s.Line(point1=(0.0, 0.0), point2=(0.0, D/2.0))
    g2 = s.Line(point1=(0.0, D/2.0), point2=(H, D/2.0))
    g3 = s.Line(point1=(H, D/2.0), point2=(H, d/2.0+r))
    g4 = s.ArcByCenterEnds(center=(H+r, d/2.0+r), point1=(H, d/2.0+r), 
        point2=(H+r, d/2.0), direction=COUNTERCLOCKWISE)
    g5 = s.Line(point1=(H+r, d/2.0), point2=(H+h, d/2.0))
    g6 = s.Line(point1=(H+h, d/2.0), point2=(H+h, 0.0))
    g7 = s.Line(point1=(H+h, 0.0), point2=(0.0, 0.0))
    p=m.Part(name='TPart',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
    p.BaseShell(sketch=s)
    #constructe the sketch to partition face
    sPartition = m.ConstrainedSketch(name='partition', sheetSize=200.0)
    g = sPartition.geometry
    g1 = sPartition.Line(point1=(0.0, d/2.0+r), point2=(H, d/2.0+r))
    g2 = sPartition.Line(point1=(0.0, d/2.0+r+dH), point2=(H, d/2.0+r+dH))
    g3 = sPartition.Line(point1=(H-dR, D/2.0), point2=(H-dR, d/2.0+r))
    g4 = sPartition.ArcByCenterEnds(center=(H+r, d/2.0+r), point1=(H-dR, d/2.0+r), 
        point2=(H+r, d/2.0-dR), direction=COUNTERCLOCKWISE)
    g5 = sPartition.Line(point1=(H+r, d/2.0-dR), point2=(H+h, d/2.0-dR))
    g6 = sPartition.Line(point1=(H+r, d/2.0), point2=(H+r, 0.0))
    g7 = sPartition.Line(point1=(H+r+dH, d/2.0), point2=(H+r+dH, 0.0))
    #build material model
    matSteel = m.Material(name='steel')
    matSteel.Elastic(table=((210000.0, 0.3), ))
    m.HomogeneousSolidSection(name='Section-steel', 
        material='steel', thickness=0.1)
    fpart = p.faces
    fT = p.Set(name='TPart', faces=fpart)
    p.SectionAssignment(region=fT, sectionName='Section-steel',
        offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    #Assembly
    a = m.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    inst = a.Instance(name='TPart-1', part=p, dependent=ON)
    eTPart = inst.edges
    edges1 = eTPart.findAt(((0.0, D/4.0, 0.0),),)
    XsymmSet = a.Set(edges=edges1, name='Xsymm')
    edges2 = eTPart.findAt((((H+h)/2., 0.0, 0.0),),)
    YsymmSet = a.Set(edges=edges2, name='Ysymm')
    side1Edges1 = eTPart.findAt(((H+h, d/4.0, 0.0),),)
    Psurface = a.Surface(side1Edges=side1Edges1, name='Surf-P')
    #Load step and boundary
    m.StaticStep(name='Load', previous='Initial')
    m.XsymmBC(name='BC-Xsymm', createStepName='Initial', region=XsymmSet)
    m.YsymmBC(name='BC-Ysymm', createStepName='Initial', region=YsymmSet)
    m.Pressure(name='Pressure', createStepName='Load', magnitude=-Press,
        region=Psurface)
    #Generate Mesh
    f = p.faces[0]
    p.PartitionFaceBySketch(faces=f, sketch=sPartition)
    eTPart = p.edges
    pEdges1 = eTPart.findAt(((H+r-cos(pi/4)*r, d/2.0+r-sin(pi/4)*r, 0.0),), 
        ((H+r-cos(pi/4)*(r+dR), d/2.0+r-sin(pi/4)*(r+dR), 0.0),))
    p.seedEdgeByNumber(edges=pEdges1, number=NumR, constraint=FIXED)
    pEdges2 = eTPart.findAt(((H-dR/2, D/2, 0),), ((H-dR/2, d/2+r, 0),),
        ((H-dR/2, d/2+r+dH, 0),), ((H+r, d/2-r/2, 0),), ((H+r+dH, d/2-r/2, 0),),
        ((H+h, d/2-r/2, 0.0),))
    p.seedEdgeByNumber(edges=pEdges2, number=NumdR, constraint=FIXED)
    pEdges3 = eTPart.findAt(((0, d/2+r+dH/2, 0),), ((H-dR, d/2+r+dH/2, 0),),
        ((H, d/2+r+dH/2, 0),), ((H+r+dH/2, 0, 0),), ((H+r+dH/2, d/2-dR, 0),),
        ((H+r+dH/2, d/2, 0),))
    p.seedEdgeByNumber(edges=pEdges3, number=NumdR, constraint=FIXED)
    p.seedPart(size=Size, deviationFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=CPS4R, secondOrderAccuracy=OFF)
    elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)
    p.setElementType(regions=fT, elemTypes=(elemType1, elemType2))
    fTPart = p.faces
    p.setMeshControls(regions=fTPart, technique=STRUCTURED, elemShape=QUAD)
    f4 = fTPart.findAt(((H/4.0, d/8.0, 0.0),),)
    p.setMeshControls(regions=f4, technique=FREE, algorithm=MEDIAL_AXIS)
    p.generateMesh()
    m.rootAssembly.regenerate()
    #Create Job
    mdb.Job(name=INPName, model=ModelName, numCpus=1)
    mdb.jobs[INPName].submit(consistencyChecking=OFF)
    mdb.jobs[INPName].waitForCompletion()
    #Print the result and extract the data
    odb = session.openOdb(name=INPName+'.odb')
    vp.setValues(displayedObject=odb)
    pth = session.Path(name='Fillet', type=CIRCUMFERENTIAL, expression=
        ((H+r, d/2+r, 10), (H+r, d/2+r, -10), (H+r, d/2, 0)), 
        circleDefinition=ORIGIN_AXIS, numSegments=16, startAngle=0, 
        endAngle=90, radius=CIRCLE_RADIUS)
    CC = odb.rootAssembly.DatumCsysByThreePoints(name='CC',origin=(H+r,d/2+r,0),
        point1=(H+r, d/2+r+1,0),point2=(H+r+1, d/2+r,0),coordSysType=CYLINDRICAL)
    vp.odbDisplay.basicOptions.setValues(transformationType=USER_SPECIFIED, 
        datumCsys=CC)
    vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
    vp.odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=
        INTEGRATION_POINT, refinement=(COMPONENT, 'S22'), )
    vp.odbDisplay.commonOptions.setValues(visibleEdges=FREE)
    vp.odbDisplay.contourOptions.setValues(spectrum='White to black')
    vp.restore()
    vp.setValues(width=120,height=80)
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
#============================generate picture===============================
phPlot = session.XYPlot(name='Fillet-element-number')
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