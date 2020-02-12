# -*- coding: mbcs -*-
import csv
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *

MkList = [HOLLOW_CIRCLE, HOLLOW_SQUARE, HOLLOW_DIAMOND, HOLLOW_TRI,
    CROSS, XMARKER, POINT]

def performCAE(dSleeveList, NumS=20):

    a_s = 30.0#shaft a
    b_s = 20.0#shaft b
    d_s = 0.1#interference value
    dList = dSleeveList
    dL_b = dList[0]#thickness of the sleeve at B end

    NumS = NumS#partition segments number
    NumEle = 3#element per segment
    theta_base = [pi/2.0*i/NumS for i in range(0, NumS+1)]
    x_shaft = [a_s*sin(theta) for theta in theta_base]
    y_shaft = [b_s*cos(theta) for theta in theta_base]
    xp_shaft = [(a_s-dL_b)*sin(theta) for theta in theta_base]
    yp_shaft = [(b_s-dL_b)*cos(theta) for theta in theta_base]
    x_sleevei = [(a_s-d_s)*sin(theta) for theta in theta_base]
    y_sleevei = [(b_s-d_s)*cos(theta) for theta in theta_base]
    pthPoints = [((a_s-d_s)*sin(i),(b_s-d_s)*cos(i),0) for i in theta_base]
    x_sleeveo, y_sleeveo = [], []
    for (i, theta) in enumerate(theta_base):
        deltaL = dList[i]
        if theta==0.0:
            x_sleeveo.append(x_sleevei[i])
            y_sleeveo.append(y_sleevei[i]+deltaL)
        elif theta==90.0:
            x_sleeveo.append(x_sleevei[i]+deltaL)
            y_sleeveo.append(y_sleevei[i])
        else:
            dy2dx = ((a_s-d_s)**2*y_sleevei[i])/((b_s-d_s)**2*x_sleevei[i])
            x_sleeveo.append(x_sleevei[i]+deltaL/sqrt(1.0+dy2dx**2))
            y_sleeveo.append(y_sleevei[i]+deltaL/sqrt(1.0+dy2dx**(-2)))
    theta_pick = [pi/2.0*(i+0.5)/NumS for i in range(0, NumS)]
    pickShaft = [((a_s*sin(i), b_s*cos(i), 0),) for i in theta_pick]
    pickSleeve = [(((a_s-d_s)*sin(i),(b_s-d_s)*cos(i),0),) for i in theta_pick]
    DxSegment = (x_sleevei[-1]-x_sleevei[-2])**2
    DySegment = (y_sleevei[-1]-y_sleevei[-2])**2
    Size = sqrt(DxSegment+DySegment)/NumEle
    modelName = 'RE'
    inpName = 'RE_Result'
    dataName = 'RE_S_1st'
    vp = session.viewports['Viewport: 1']
    Mdb()
    m = mdb.Model(name=modelName)
    #Sketch and part
    s_shaft = m.ConstrainedSketch(name='shaft', sheetSize=200.0)
    g1 = s_shaft.EllipseByCenterPerimeter(center=(0.0, 0.0), axisPoint1=
        (a_s, 0.0), axisPoint2=(0.0, -b_s))
    g2 = s_shaft.Line(point1=(0.0, 0.0), point2=(0.0, b_s))
    g3 = s_shaft.Line(point1=(0.0, 0.0), point2=(a_s, 0.0))
    s_shaft.autoTrimCurve(curve1=g1, point1=(-a_s, 0.0))
    Shaft = m.Part(name='Shaft', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    Shaft.BaseShell(sketch=s_shaft)

    s_sleeve = m.ConstrainedSketch(name='sleeve', sheetSize=200.0)
    g1 = s_sleeve.EllipseByCenterPerimeter(center=(0.0, 0.0), axisPoint1=
        (a_s-d_s, 0.0), axisPoint2=(0.0, -b_s+d_s))
    SPoints = zip(x_sleeveo, y_sleeveo)
    g2 = s_sleeve.Spline(points=SPoints)
    g3 = s_sleeve.Line(point1=(0, b_s-d_s), point2=SPoints[0])
    g4 = s_sleeve.Line(point1=(a_s-d_s, 0), point2=SPoints[-1])
    s_sleeve.autoTrimCurve(curve1=g1, point1=(-a_s+d_s, 0))
    Sleeve = m.Part(name='Sleeve', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
    Sleeve.BaseShell(sketch=s_sleeve)

    SP_shaft = m.ConstrainedSketch(name='SP_shaft', sheetSize=200.0)
    g1 = SP_shaft.EllipseByCenterPerimeter(center=(0.0, 0.0), axisPoint1=
        ((a_s-dL_b), 0.0), axisPoint2=(0.0, -(b_s-dL_b)))
    PointsIn, PointsOut = zip(xp_shaft, yp_shaft), zip(x_shaft, y_shaft)
    for i in range(len(theta_base)):
        SP_shaft.Line(point1=PointsIn[i], point2=PointsOut[i])

    SP_sleeve = m.ConstrainedSketch(name='SP_sleeve', sheetSize=200.0)
    PointsIn, PointsOut = zip(x_sleevei, y_sleevei), zip(x_sleeveo, y_sleeveo)
    for i in range(len(theta_base)):
        SP_sleeve.Line(point1=PointsIn[i], point2=PointsOut[i])

    #build material model
    matSteel = m.Material(name='steel')
    matSteel.Elastic(table=((210000.0, 0.3), ))
    m.HomogeneousSolidSection(name='Section-steel', 
        material='steel', thickness=1)
    matBrit = m.Material(name='Brit')
    matBrit.Elastic(table=((100000.0, 0.3), ))
    m.HomogeneousSolidSection(name='Section-Brit', 
        material='Brit', thickness=1)
    faceShaft = Shaft.faces
    faceShaft = Shaft.Set(name='shaft', faces=faceShaft)
    Shaft.SectionAssignment(region=faceShaft, sectionName='Section-steel')
    faceSleeve = Sleeve.faces
    faceSleeve = Sleeve.Set(name='sleeve', faces=faceSleeve)
    Sleeve.SectionAssignment(region=faceSleeve, sectionName='Section-Brit')
    #Assembly
    root = m.rootAssembly
    root.DatumCsysByDefault(CARTESIAN)
    InstShaft = root.Instance(name='Shaft-1', part=Shaft, dependent=ON)
    InstSleeve = root.Instance(name='sleeve-1', part=Sleeve, dependent=ON)
    edgeShaft = InstShaft.edges
    edges1 = edgeShaft.findAt(((a_s*sin(pi/4), b_s*cos(pi/4), 0.0),),)
    edgesX1 = edgeShaft.findAt(((0.0, b_s/2.0, 0.0),),)
    edgesY1 = edgeShaft.findAt(((a_s/2.0, 0.0, 0.0),),)
    shaftSurface = root.Surface(side1Edges=edges1, name='shaftSurface')
    edgeSleeve = InstSleeve.edges
    edges2 = edgeSleeve.findAt((((a_s-d_s)*sin(pi/4), 
        (b_s-d_s)*cos(pi/4), 0.0),),)
    edgesX2 = edgeSleeve.findAt(((0.0, (b_s-d_s+dL_b/10), 0.0),),)
    edgesY2 = edgeSleeve.findAt((((a_s-d_s+dL_b/10), 0.0, 0.0),),)
    sleeveSurface = root.Surface(side1Edges=edges2, name='sleeveSurface')
    XsymmSet = root.Set(edges=edgesX1+edgesX2, name='Xsymm')
    YsymmSet = root.Set(edges=edgesY1+edgesY2, name='Ysymm')
    #Load step and boundary
    m.StaticStep(name='Load', previous='Initial')
    m.XsymmBC(name='BC-Xsymm', createStepName='Initial', region=XsymmSet)
    m.YsymmBC(name='BC-Ysymm', createStepName='Initial', region=YsymmSet)
    intProp = m.ContactProperty('IntProp-1')
    intProp.TangentialBehavior(formulation=FRICTIONLESS)
    m.SurfaceToSurfaceContactStd(name='Int-1', createStepName='Load', 
        master=sleeveSurface, slave=shaftSurface, sliding=FINITE, thickness=ON, 
        interactionProperty='IntProp-1', interferenceType=SHRINK_FIT)
    #Partition and Mesh
    Shaft.PartitionFaceBySketch(faces=Shaft.faces[0], sketch=SP_shaft)
    Sleeve.PartitionFaceBySketch(faces=Sleeve.faces[0], sketch=SP_sleeve)
    eShaft = Shaft.edges
    pEdges = eShaft.findAt(*pickShaft)
    Shaft.seedEdgeByNumber(edges=pEdges, number=NumEle, constraint=FIXED)
    pEdges = eShaft.findAt(((0, b_s/2, 0),),((a_s/2, 0, 0),))
    Shaft.seedEdgeBySize(edges=pEdges, size=3.0*Size, constraint=FINER)
    eSleeve = Sleeve.edges
    pEdges = eSleeve.findAt(*pickSleeve)
    Sleeve.seedEdgeByNumber(edges=pEdges, number=NumEle, constraint=FIXED)
    Shaft.seedPart(size=Size, deviationFactor=0.1)
    Sleeve.seedPart(size=Size, deviationFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=CPE4, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
    fShaft = Shaft.faces
    Shaft.setElementType(regions=(fShaft, ), elemTypes=(elemType1, elemType2))
    fSleeve = Sleeve.faces
    Sleeve.setElementType(regions=(fSleeve, ), elemTypes=(elemType1, elemType2))
    Shaft.generateMesh()
    Sleeve.generateMesh()
    m.rootAssembly.regenerate()
    #submit and Post-process
    m.setValues(noPartsInputFile=OFF)
    job = mdb.Job(name=inpName, model=modelName, numCpus=2, numDomains=2)
    job.submit(consistencyChecking=OFF)
    job.waitForCompletion()
    odb = session.openOdb(name=inpName+'.odb')
    vp.setValues(displayedObject=odb)
    vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
    vp.odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=
        INTEGRATION_POINT, refinement=(INVARIANT, 'Max. Principal'), )
    vp.odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, 
        visibleEdges=FREE, uniformScaleFactor=1)
    leaf = dgo.LeafFromPartInstance(partInstanceName=('SLEEVE-1', ))
    vp.odbDisplay.displayGroup.replace(leaf=leaf)
    pth = session.Path(name='Fillet', type=POINT_LIST, expression=pthPoints)
    data = session.XYDataFromPath(name=dataName, path=pth, shape=UNDEFORMED,
        includeIntersections= False, labelType=TRUE_DISTANCE)
    Stress = zip(*data.data)[1]
    Distance = zip(*data.data)[0]
    output, Dist = [], []
    for (i, item) in enumerate(Distance):
        if item not in Dist:
            Dist.append(item)
            output.append(Stress[i])
    return output

# now a func to run the iteration
def iterateShape(init, NumSeg, upLimit=50, sigma=0.2):
    shape0 = shapePre =init
    result0 = resultPre = init
    Sdata0 = SdataPre = 1000.0    
    upLimit = upLimit
    NumS = NumSeg
    sigma = sigma
    outFile = csv.writer(file('out.csv', 'wb'))
    i = 0

    theta_base = [90.0*m/NumS for m in range(0, NumS+1)]
    shape2Plot, result2Plot = [], []
    while i<upLimit:
        # execute a iteration
        try:
            refer = resultPre[0]
            relatiValue = [item/refer-1.0 for item in resultPre]
            shape0 = [shapePre[k]*(1.0+item*sigma) for (k, item) in \
                enumerate(relatiValue)]
            result0 = performCAE(shape0, NumS)
            Sdata0 = max(result0)-min(result0)
            infor = 'Normal interation'
            q = 1
            while Sdata0>=SdataPre:
                sigma = 0.5*sigma
                infor = 'Cutback occurs: decrease sigma '
                refer = resultPre[0]
                relatiValue = [item/refer-1.0 for item in resultPre]
                #update shape value according to previous stress result
                shape0 = [shapePre[k]*(1+item*sigma) for (k, item) \
                    in enumerate(relatiValue)]
                result0 = performCAE(shape0, NumS)
                Sdata0 = max(result0)-min(result0)
                q+=1
                if q>3: break
                
            shape2Plot.append(zip(theta_base, shape0))
            result2Plot.append(zip(theta_base, result0))
            #keep the log information
            outStr0 = ['Iter'+str(i), infor, 'sigma=' + str(sigma)]
            outStr1 = ['shapeValue=']
            [outStr1.append(item) for item in shape0]
            outStr2 = ['stressValue=']
            [outStr2.append(item) for item in result0]
            outStr2.append(Sdata0)
            outFile.writerow(outStr0)
            outFile.writerow(outStr1)
            outFile.writerow(outStr2)
            #update shape value according to current stress result
            shapePre = shape0
            resultPre = result0
            SdataPre = Sdata0
            i+=1

        except BaseException, e:
            break
            strE = ['Iter'+str(i), 'Failure caused by '+ str(e),\
                'Cutback occurs!']
            outStr2 = ['stressValue=']
            [outStr2.append(item) for item in result0]
            outFile.writerow(strE)
            outFile.writerow(outStr2)
            sigma = 0.5*sigma
            i+=1

    return shape2Plot, result2Plot

if __name__ == '__main__':
    NumS = 20
    initShape = [2.0]*(NumS+1)
    limit = 24
    sigma = 0.2
    datas = iterateShape(initShape, NumS, limit, sigma)
    curveResults, curveShapes = [], []
    vp = session.viewports['Viewport: 1']
    for j in range(0,6,1):
        dataShape=session.XYData(data=datas[0][4*j],name='Iter'+str(4*j),\
            xValuesLabel='Angle', yValuesLabel='Width (mm)')
        curveShape = session.Curve(xyData=dataShape)
        curveShape.setValues(displayTypes=(SYMBOL,),legendLabel='Iter'\
            +str(4*j), useDefault=OFF)
        curveShape.symbolStyle.setValues(marker=MkList[j],size=1.5, \
            color='Black')
        curveShapes.append(curveShape)
    #=========================generate shape picture=====================
    
    phPlot1 = session.XYPlot(name='XYPlot-iteration shape history')
    phPlot1.title.setValues(text='Iteration History: Shape')
    chartName = phPlot1.charts.keys()[0]
    chart = phPlot1.charts[chartName]
    chart.setValues(curvesToPlot=curveShapes, )
    chart.gridArea.style.setValues(color='White')
    chart.legend.area.style.setValues(color='Gray')
    phPlot1.title.style.setValues(
        font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
    chart.legend.textStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.legend.titleStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.axes1[0].labelStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.axes1[0].titleStyle.setValues(
        font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
    chart.axes2[0].labelStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.axes2[0].titleStyle.setValues(
        font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
    chart.axes1[0].axisData.setValues(maxValue=90, minValue=0,
        maxAutoCompute=False, minAutoCompute=False)
    chart.axes1[0].axisData.setValues(tickIncrement=18, tickMode=INCREMENT)
    vp.setValues(width=180,height=150,origin=(0,-20))
    vp.setValues(displayedObject=phPlot1)
    session.printOptions.setValues(rendition=GREYSCALE, vpDecorations=OFF, 
        reduceColors=False)
    session.printToFile(fileName='IterShapes', format=TIFF, 
        canvasObjects=( vp, ))
    #==================================================================
    for j in range(0, 6, 1):
        dataResult= session.XYData(data=datas[1][4*j],name='Iter'+str(4*j),\
            xValuesLabel='Angle', yValuesLabel='1st Prinipal Stress (Mpa)')
        curveResult = session.Curve(xyData=dataResult)
        curveResult.setValues(displayTypes=(SYMBOL,),legendLabel='Iter'\
            +str(4*j), useDefault=OFF)
        curveResult.symbolStyle.setValues(marker=MkList[j],size=1.5, \
            color='Black')
        curveResults.append(curveResult)
    #========================generate stress picture====================
    phPlot2 = session.XYPlot(name='XYPlot-iteration stress history')
    phPlot2.title.setValues(text='Iteration History: Stress')
    chartName = phPlot2.charts.keys()[0]
    chart = phPlot2.charts[chartName]
    chart.setValues(curvesToPlot=curveResults, )
    chart.gridArea.style.setValues(color='White')
    chart.legend.area.style.setValues(color='Gray')
    phPlot2.title.style.setValues(
        font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
    chart.legend.textStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.legend.titleStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.axes1[0].labelStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.axes1[0].titleStyle.setValues(
        font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
    chart.axes2[0].labelStyle.setValues(
        font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
    chart.axes2[0].titleStyle.setValues(
        font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
    chart.axes1[0].axisData.setValues(maxValue=90, minValue=0,
        maxAutoCompute=False, minAutoCompute=False)
    chart.axes1[0].axisData.setValues(tickIncrement=18, tickMode=INCREMENT)
    #=============================print result===========================
    vp.setValues(width=180,height=150,origin=(0,-20))
    vp.setValues(displayedObject=phPlot2)
    session.printOptions.setValues(rendition=GREYSCALE, vpDecorations=OFF, 
        reduceColors=False)
    session.printToFile(fileName='IterResult', format=TIFF, 
        canvasObjects=( vp, ))