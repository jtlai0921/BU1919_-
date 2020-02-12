# -*- coding: mbcs -*-
import pickle
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
#from utility import getByRadius

def getByRadius (source, radius, tol=1e-3):
    result={'Edge':[], 'coordY':[], 'coordX':[]}
    vets = source.vertices
    for e in source.edges:
        try:
            if abs(e.getRadius()-radius)<tol and abs(e.pointOn[0][2])<tol:
                vList = e.getVertices()
                result['Edge'].append(e)
                for idi in vList:
                    data = vets[idi].pointOn[0]
                    result['coordY'].append(data[1])
                    result['coordX'].append(data[0])
        except Exception as e:
            print e
    return result

def getForce(numbers, thickness, RName = ''):
    Nbul = numbers#total number of bulge
    t0 = thickness#thickness of the pen/cover

    Abula = 20#effective angle of one bulge
    L1 = 25.0#length of cover
    L3 = 3.0#length of entry in cover
    R1 = 6.0#inner radius of the cover
    t1 = t0#thickness of the cover

    L4 = 25.0#length of pen
    L5 = 4.0#length of entry in pen
    t3 = t0#thickness of the pen
    L6 = 6.0#length of cut in pen

    L2 = 3.0#length of bulge region
    aph1 = 15.0#entry slop angle
    aph2 = 15.0#exit slop angle

    Abul = Abula/180.0*pi
    aph1 = aph1/180.0*pi
    aph2 = aph2/180.0*pi
    t2 = L2/(1.0/tan(aph1)+1.0/tan(aph2))#raw height of the bulge
    rdFt = 1.0
    ModelName = 'penModel'
    INPName = 'penINP' + RName
    Mdb()

    md = mdb.Model(name=ModelName)
    #Generate part-Cover geometry
    s1 = md.ConstrainedSketch(name='cover', sheetSize=200.0)
    g1 = s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    c1 = s1.FixedConstraint(entity=g1)
    g2 = s1.Line(point1=(R1, L1), point2=(R1, L2+L3))
    point = (R1-t2, L2+L3-t2/tan(aph2))
    g3 = s1.Line(point1=(R1, L2+L3), point2=point)
    g4 = s1.Line(point1=point, point2=(R1, L3))
    g5 = s1.Line(point1=(R1, L3), point2=(R1, 0.0))
    g6 = s1.Line(point1=(R1, 0.0), point2=(R1+t1, 0.0))
    g7 = s1.Line(point1=(R1+t1, 0.0), point2=(R1+t1, L1))
    g8 = s1.Line(point1=(R1+t1, L1), point2=(R1, L1))
    g9 = s1.FilletByRadius(radius=rdFt, curve1=g3, nearPoint1=point, 
        curve2=g4, nearPoint2=point)
    pCover = md.Part(name='cover', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    pCover.BaseSolidRevolve(sketch=s1, angle=360.0/Nbul/2.0, 
        flipRevolveDirection=OFF)
    #Generate part-pen geometry
    s2 = md.ConstrainedSketch(name='pen', sheetSize=200.0)
    g1 = s2.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    c1 = s2.FixedConstraint(entity=g1)
    baseX, baseY = R1-t2, L2+L3-t2/tan(aph2)
    g2 = s2.Line(point1=(baseX, baseY), point2=(R1, L3))
    g3 = s2.Line(point1=(R1, L3), point2=(baseX, L3-t2/tan(aph2)))
    baseY2 = -1.0*(L4-L5-t2/tan(aph1)-L3)
    g4 = s2.Line(point1=(baseX, L3-t2/tan(aph2)), point2=(baseX, baseY2))
    g5 = s2.Line(point1=(baseX, baseY2), point2=(baseX-t3, baseY2))
    g6 = s2.Line(point1=(baseX-t3, baseY2), point2=(baseX-t3, baseY2+L4))
    g7 = s2.Line(point1=(baseX-t3, baseY2+L4), point2=(baseX, baseY2+L4))
    g8 = s2.Line(point1=(baseX, baseY2+L4), point2=(baseX, baseY))
    g9 = s2.FilletByRadius(radius=rdFt, curve1=g2, nearPoint1=(R1, L3), 
        curve2=g3, nearPoint2=(R1, L3))
    pPen = md.Part(name='pen', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    pPen.BaseSolidRevolve(sketch=s2, angle=360.0/Nbul/2.0, 
        flipRevolveDirection=OFF)
    dat = pPen.datums
    pd1 = pPen.DatumPointByCoordinate(coords=(20.0*cos(pi/Nbul),
        0.0,20.0*sin(pi/Nbul)))
    axis1 = pPen.DatumAxisByPrincipalAxis(principalAxis=YAXIS)
    plane1 = pPen.DatumPlaneByLinePoint(line=dat[axis1.id],
        point=dat[pd1.id])
    tf = pPen.MakeSketchTransform(sketchPlane=dat[plane1.id], 
        sketchUpEdge=dat[axis1.id], sketchPlaneSide=SIDE2, 
        sketchOrientation=LEFT, origin=(0.0,baseY-L2/2.0,0.0))
    sCut = md.ConstrainedSketch(name='Scut',sheetSize=200, transform=tf)
    g1 = sCut.rectangle(point1=(0.0, -L6/2.0), 
        point2=(baseX+2.0, L6/2.0))
    g2 = sCut.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    sCut.assignCenterline(line=g2)
    pPen.CutRevolve(sketchPlane=dat[plane1.id], sketchPlaneSide=SIDE2,
        sketchUpEdge=dat[axis1.id], sketchOrientation=LEFT, sketch=sCut,
        angle=180.0/Nbul-Abula/2.0)
    #define the material and assign the section to the parts
    matPlastic = md.Material(name='Plastic')
    matPlastic.Elastic(table=((2300.0, 0.35), ))
    matPlastic.Density(table=((1e-09, ), ))
    md.HomogeneousSolidSection(name='Sec', material='Plastic', 
        thickness=None)
    c = pCover.cells
    cCover = pCover.Set(name='cCover', cells=c)
    pCover.SectionAssignment(region=cCover, sectionName='Sec')
    c = pPen.cells
    cPen = pPen.Set(name='cPen', cells=c)
    pPen.SectionAssignment(region=cPen, sectionName='Sec')
    #Assembly the model and define the steps
    root = md.rootAssembly
    root.DatumCsysByDefault(CARTESIAN)
    instPen = root.Instance(name='Pen', part=pPen, dependent=ON)
    instCov = root.Instance(name='Cover', part=pCover, dependent=ON)
    md.StaticStep(name='Step', previous='Initial', 
        maxNumInc=1000, initialInc=0.1, maxInc=0.1)
    md.fieldOutputRequests['F-Output-1'].setValues(numIntervals=10)
    #define the contact
    fcs1 = instPen.faces
    point1 = (0, baseY-L2/2.0+L6/2.0-1.0, 0)
    point2 = (0, baseY-L2/2.0-L6/2.0+1.0, 0)
    sFaces1 = fcs1.getByBoundingCylinder(center1=point1, center2=point2, 
        radius=R1+2.0)
    surf1 = root.Surface(side1Faces=sFaces1, name='Surf1')
    fcs2 = instCov.faces
    point1 = (0, L3, 0)
    point2 = (0, L2+L3, 0)
    sFaces2 = fcs2.getByBoundingCylinder(center1=point1, center2=point2, 
        radius=R1+2.0)
    surf2 = root.Surface(side1Faces=sFaces2, name='Surf2')
    conProp = md.ContactProperty('IntProp-1')
    conProp.TangentialBehavior(formulation=PENALTY, table=((0.1, ), ),
        maximumElasticSlip=FRACTION, fraction=0.005)
    md.SurfaceToSurfaceContactStd(name='Int-1', createStepName='Initial', 
        master=surf2, slave=surf1, sliding=FINITE, 
        interactionProperty='IntProp-1')
    #define the loads and boundaries
    Csys = root.DatumCsysByThreePoints(name='cDatum', coordSysType=CYLINDRICAL,
        origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, 1.0))
    ang = pi/Nbul
    xC1, yC1, zC1 = R1+t1/2.0, L1/2.0, 0.0
    xC2, yC2, zC2 = xC1*cos(ang), L1/2.0, xC1*sin(ang)
    fc1 = fcs2.findAt(((xC1, yC1, zC1),),)
    fc2 = fcs2.findAt(((xC2, yC2, zC2),),)
    fc3 = fcs2.findAt(((xC1*cos(ang/2.0), L1, xC1*sin(ang/2.0)),),)
    xC1, yC1, zC1 = R1-t2-t3/2.0, baseY+(2*L5-2*L4-L6-L2)/4.0, 0.0
    xC2, yC2, zC2 = xC1*cos(ang), baseY+(L6-L2+2*L5)/4.0, xC1*sin(ang)
    fp1 = fcs1.findAt(((xC1, yC1, zC1),),)
    fp2 = fcs1.findAt(((xC2, yC2, zC2),),((xC2, yC1, zC2),))
    fp3 = fcs1.findAt(((xC2, baseY+L5-L4, zC2),),)
    sym1 = root.Set(name='sym1', faces=fc1+fp1)
    sym2 = root.Set(name='sym2', faces=fc2+fp2)
    Fixs = root.Set(name='Fixs', faces=fc3)
    Push = root.Set(name='push', faces=fp3)
    datum = root.datums[Csys.id]
    xrp, zrp = (R1+t1/2.0)*cos(pi/Nbul/2.0), (R1+t1/2.0)*sin(pi/Nbul/2.0)
    rp = root.ReferencePoint(point=(xrp, L1, zrp))
    rps = root.referencePoints
    RPSet = root.Set(referencePoints=(rps[rp.id],), name='RPSet')
    md.Coupling(name='coupling', controlPoint=RPSet, surface=Fixs, u3=ON, 
        influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=datum)
    md.DisplacementBC(name='sym-1', createStepName='Initial', 
        region=sym1, u2=SET, ur1=SET, ur3=SET, localCsys=datum)
    md.DisplacementBC(name='sym-2', createStepName='Initial', 
        region=sym2, u2=SET, ur1=SET, ur3=SET, localCsys=datum)
    md.DisplacementBC(name='Fix', createStepName='Initial', 
        region=RPSet, u3=SET, localCsys=datum)
    #partition part-Pen
    datPen = pPen.datums
    planes = []
    pd2 = pPen.DatumPointByCoordinate(coords=(20.0*cos(Abul/2.0),
        0.0,20.0*sin(Abul/2.0)))
    planes.append(pPen.DatumPlaneByLinePoint(line=datPen[axis1.id],
        point=datPen[pd2.id]).id)
    pd3 = pPen.DatumPointByCoordinate(coords=(0.0, 
        baseY+(L6-L2)/2.0, 0.0))
    pd4 = pPen.DatumPointByCoordinate(coords=(0.0, 
        baseY-L2-(L6-L2)/2.0, 0.0))
    planes.append(pPen.DatumPlaneByPointNormal(point=datPen[pd3.id],
        normal=datPen[axis1.id]).id)
    planes.append(pPen.DatumPlaneByPointNormal(point=datPen[pd4.id],
        normal=datPen[axis1.id]).id)
    pd5 = pPen.DatumPointByCoordinate(coords=(0.0, baseY, 0.0))
    pd6 = pPen.DatumPointByCoordinate(coords=(0.0, baseY-L2, 0.0))
    planes.append(pPen.DatumPlaneByPointNormal(point=datPen[pd5.id],
        normal=datPen[axis1.id]).id)
    planes.append(pPen.DatumPlaneByPointNormal(point=datPen[pd6.id],
        normal=datPen[axis1.id]).id)
    result = getByRadius(pPen, rdFt)
    coorY, coorX= result['coordY'], result['coordX']
    coorde = result['Edge'][0].pointOn[0]
    pd7 = pPen.DatumPointByCoordinate(coords=(0.0, coorY[0], 0.0))
    pd8 = pPen.DatumPointByCoordinate(coords=(0.0, coorY[1], 0.0))
    planes.append(pPen.DatumPlaneByPointNormal(point=datPen[pd7.id],
        normal=datPen[axis1.id]).id)
    planes.append(pPen.DatumPlaneByPointNormal(point=datPen[pd8.id],
        normal=datPen[axis1.id]).id)
    for idi in planes:
        datPen = pPen.datums
        cls = pPen.cells
        pPen.PartitionCellByDatumPlane(datumPlane=datPen[idi], cells=cls)
    #Mesh the part-Pen
    egs1 = pPen.edges
    x, y1, y2, y3, y4 = R1-t2-t3/2 ,baseY, coorY[1], coorY[0], baseY-L2
    eg1 = egs1.findAt(((x,y1,0),),((x,y2,0),),((x,y3,0),),((x,y4,0),))
    pPen.seedEdgeByNumber(edges=eg1, number=4, constraint=FIXED)
    eg2 = egs1.findAt(((R1-t2-t3, coorde[1],0),), (coorde,))
    pPen.seedEdgeByNumber(edges=eg2, number=4, constraint=FIXED)
    x1, x2 = (coorX[0]+R1-t2)/2.0, (coorX[1]+R1-t2)/2.0
    if coorY[0]<coorY[1]:
        y1, y2 = (coorY[0]+baseY-L2)/2.0, (coorY[1]+baseY)/2.0
    else:
        y1, y2 = (coorY[0]+baseY)/2.0, (coorY[1]+baseY-L2)/2.0
    eg3 = egs1.findAt(((x1,y1,0),),((R1-t2-t3,y1,0),),)
    eg4 = egs1.findAt(((x2,y2,0),),((R1-t2-t3,y2,0),),)
    pPen.seedEdgeByNumber(edges=eg3, number=8, constraint=FIXED)
    pPen.seedEdgeByNumber(edges=eg4, number=8, constraint=FIXED)
    eg5 = egs1.findAt((((R1-t2)*cos(Abul/4.0),baseY,(R1-t2)*sin(Abul/4.0)),),)
    pPen.seedEdgeByNumber(edges=eg5, number=5, constraint=FIXED)
    pPen.seedPart(size=0.4, deviationFactor=0.1)
    pPen.generateMesh()
    #partition the part-Cover
    datCover = pCover.datums
    planes = []
    pd2 = pCover.DatumPointByCoordinate(coords=(20.0*cos(Abul/2.0),
        0.0,20.0*sin(Abul/2.0)))
    axis1 = pCover.DatumAxisByPrincipalAxis(principalAxis=YAXIS)
    planes.append(pCover.DatumPlaneByLinePoint(line=datCover[axis1.id],
        point=datCover[pd2.id]).id)
    pd3 = pCover.DatumPointByCoordinate(coords=(0.0, L3, 0.0))
    pd4 = pCover.DatumPointByCoordinate(coords=(0.0, L3+L2, 0.0))
    planes.append(pCover.DatumPlaneByPointNormal(point=datCover[pd3.id],
        normal=datCover[axis1.id]).id)
    planes.append(pCover.DatumPlaneByPointNormal(point=datCover[pd4.id],
        normal=datCover[axis1.id]).id)
    result = getByRadius(pCover, rdFt)
    coorY, coorX= result['coordY'], result['coordX']
    coorde = result['Edge'][0].pointOn[0]
    pd5 = pCover.DatumPointByCoordinate(coords=(0.0, coorY[0], 0.0))
    pd6 = pCover.DatumPointByCoordinate(coords=(0.0, coorY[1], 0.0))
    planes.append(pCover.DatumPlaneByPointNormal(point=datCover[pd5.id],
        normal=datCover[axis1.id]).id)
    planes.append(pCover.DatumPlaneByPointNormal(point=datCover[pd6.id],
        normal=datCover[axis1.id]).id)
    for idi in planes:
        cls = pCover.cells
        pCover.PartitionCellByDatumPlane(datumPlane=datCover[idi], cells=cls)
    #Mesh the part-Cover
    pCover.seedPart(size=0.4, deviationFactor=0.1)
    egs1 = pCover.edges
    x, y1, y2, y3, y4 = R1+t1/2.0 ,L3, coorY[1], coorY[0], L3+L2
    eg1 = egs1.findAt(((x,y1,0),),((x,y2,0),),((x,y3,0),),((x,y4,0),))
    pCover.seedEdgeByNumber(edges=eg1, number=4, constraint=FIXED)
    eg2 = egs1.findAt(((R1+t1, coorde[1],0),), (coorde,))
    pCover.seedEdgeByNumber(edges=eg2, number=4, constraint=FIXED)
    x1, x2, Lmv = (coorX[0]+R1)/2.0, (coorX[1]+R1)/2.0, 0.0
    if coorY[0]<coorY[1]:
        y1, y2 = (coorY[0]+L3)/2.0, (coorY[1]+L3+L2)/2.0
        Lmv = coorY[1]-L3
    else:
        y1, y2 = (coorY[0]+L3+L2)/2.0, (coorY[1]+L3)/2.0
        Lmv = coorY[0]-L3
    eg3 = egs1.findAt(((x1,y1,0),),((R1+t1,y1,0),),)
    eg4 = egs1.findAt(((x2,y2,0),),((R1+t1,y2,0),),)
    pCover.seedEdgeByNumber(edges=eg3, number=8, constraint=FIXED)
    pCover.seedEdgeByNumber(edges=eg4, number=8, constraint=FIXED)
    eg5 = egs1.findAt(((R1*cos(Abul/4.0),L3,R1*sin(Abul/4.0)),),)
    pCover.seedEdgeByNumber(edges=eg5, number=5, constraint=FIXED)
    pCover.generateMesh()
    #Disp boundary
    md.DisplacementBC(name='Push', createStepName='Step', 
        region=Push, u3=-Lmv, localCsys=datum)
    root.regenerate()
    #Job and submit
    job = mdb.Job(name=INPName, model=ModelName, numCpus=2, numDomains=2)
    Result = 0.0
    try:
        job.submit(consistencyChecking=OFF)
        job.waitForCompletion()
        odb = session.openOdb(name=INPName+'.odb')
        session.viewports['Viewport: 1'].setValues(displayedObject=odb)
        xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, 
            variable=(('RF', NODAL, ((COMPONENT, 'RF2'), )), ), 
            nodeSets=('RPSET', ))
        data = xyList[0].data
        Result = abs(min(zip(*data)[1]))

    except BaseException, e:
        Result = -1.0

    return Result*Nbul

if __name__=='__main__':
    numLimit, thkLimit, nDiv = 12, 1.2, 3
    numbers, thickes, results = [], [], []
    for i in range(1,nDiv+1):
        for j in range(1,nDiv+1):
            numi = numLimit*i/nDiv
            thki = thkLimit*j/nDiv
            numbers.append(numi)
            thickes.append(thki)
            results.append(getForce(numi, thki, str(i)+str(j)))

    output = open('data.pkl', 'wb')
    pickle.dump(numbers, output)
    pickle.dump(thickes, output)
    pickle.dump(results, output)
    output.close()
