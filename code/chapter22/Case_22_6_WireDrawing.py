# -*- coding: mbcs -*-
import os, sys, os.path, pickle
import xlrd
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbAccess import *

def getDataFromExcel(sourceFile, Num):
    '''Read parameter from Excel'''
    cur_path = os.path.abspath('.')#os.getcwd()
    para_path = os.path.join(cur_path, sourceFile)
    datas = xlrd.open_workbook(para_path)
    sh = datas.sheet_by_name('ProcessParameters')
    Di_s = []
    Do_s = []
    Rd_s = []
    for i in range(1,Num+1):
        Di_s.append(sh.cell_value(i, 1))
        Do_s.append(sh.cell_value(i, 2))
        Rd_s.append(sh.cell_value(i, 3)/180.0*pi)
    
    return (Di_s,Do_s,Rd_s)

def wireDrawing(Di_s,Do_s,Rd_s,fric = 0.05,Ratio = 4.0):
    '''Perform simulation and return result'''
    Mdb()
    Ratio = Ratio #initial wire length/diameter
    Delta = 1.1 #Die entry Diameter increase
    HoldL = 0.5 #bearing length
    fric = fric
    ForceL = []#drawing force of each pass
    DoRL = []#output drawing wire
    S22Data = []#residual stress after drawing
    Di_init = Di_s[0]
    vp = session.viewports['Viewport: 1']
    oldJob = ''
    DispL = []
    unitL = 1.0#mm
    UnitEnergy = 0
    Num = len(Di_s)
    leng = unitL
    for i in range(Num):
        modelName = 'wireDrawing'+str(i+1)
        Di = Di_init
        Do = Do_s[i]
        Rd = Rd_s[i]
        press = 1.0
        DieDraw = mdb.Model(name=modelName)
        #wire
        sWire = DieDraw.ConstrainedSketch(name='wire', sheetSize=200.0)
        sWire.sketchOptions.setValues(viewStyle=AXISYM)
        sWire.setPrimaryObject(option=STANDALONE)
        sWire.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        sWire.Line(point1=(Di/2.0, 0.0), point2=(Di/2.0, Di*Ratio))
        sWire.Line(point1=(Di/2.0, Di*Ratio), point2=(0.0, Di*Ratio))
        sWire.Line(point1=(0.0, Di*Ratio), point2=(0.0, 0.0))
        sWire.Line(point1=(0.0, 0.0), point2=(Di/2.0, 0.0))
        pWire = DieDraw.Part(name='wire', dimensionality=AXISYMMETRIC, 
            type=DEFORMABLE_BODY)
        pWire.BaseShell(sketch=sWire)
        sWire.unsetPrimaryObject()
        #die1
        posY1 = (Di*Delta-Di)/2.0/tan(Rd)
        posY2 = -1.0*(Di-Do)/2.0/tan(Rd)
        sDie = DieDraw.ConstrainedSketch(name='die', sheetSize=200.0)
        sDie.sketchOptions.setValues(viewStyle=AXISYM)
        sDie.setPrimaryObject(option=STANDALONE)
        sDie.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
        sDie.Line(point1=(Di*Delta/2.0, posY1), point2=(Do/2.0, posY2))
        sDie.Line(point1=(Do/2.0, posY2), point2=(Do/2.0, posY2-HoldL))
        pDie = DieDraw.Part(name='die', dimensionality=AXISYMMETRIC, 
            type=ANALYTIC_RIGID_SURFACE)
        pDie.AnalyticRigidSurf2DPlanar(sketch=sDie)
        sDie.unsetPrimaryObject()
        Disp = Di*Ratio*(Di/Do)**2 + HoldL + abs(posY2)
        DispL.append(Disp - abs(posY2))
        #material
        mat = DieDraw.Material(name='steel')
        mat.Elastic(table=((200000.0, 0.3), ))
        mat.Plastic(table=((1359.0, 0.0), (1918.0, 1.60)))
        mat.Density(table=((7.86e-09, ), ))
        DieDraw.HomogeneousSolidSection(name='Sect', material='steel')
        fWire = pWire.faces
        fSet = pWire.Set(name='wire', faces=fWire)
        pWire.SectionAssignment(region=fSet, sectionName='Sect')
        #Instance
        root = DieDraw.rootAssembly
        iWire = root.Instance(name='wire', part=pWire, dependent=ON)
        iDie = root.Instance(name='die', part=pDie, dependent=ON)
        #steps
        DieDraw.StaticStep(name='drawing', previous='Initial', timePeriod=1.0,
            maxNumInc=10000, initialInc=0.002, minInc=1e-6, maxInc=0.003, nlgeom=ON)
        DieDraw.steps['drawing'].Restart(frequency=0, numberIntervals=1, 
            overlay=ON, timeMarks=OFF)
        #Set and surface
        sWire = iWire.edges
        sideEdges = sWire.findAt(((Di/2.0, Di*Ratio/2.0, 0.0),),)
        conS = root.Surface(side1Edges=sideEdges, name='wire')
        BCEdge = sWire.findAt(((Di/4.0, 0.0, 0.0),),)
        MoveBC = root.Set(name='move', edges=BCEdge)
        AXISEdge = sWire.findAt(((0.0, Di*Ratio/2.0, 0.0),),)
        AXISBC = root.Set(name='AXIS', edges=AXISEdge)
        sDie = iDie.edges
        sideEdges = sDie.findAt(((Do/2.0, posY2-HoldL/2.0, 0.0),),)
        conM = root.Surface(side2Edges=sideEdges, name='die')
        refP1 = root.ReferencePoint(point=(0.0,0.0,0.0))
        refP2 = root.ReferencePoint(point=(Do/2.0, posY2, 0.0))
        refPs = root.referencePoints
        refDie = root.Set(referencePoints=(refPs[refP2.id],), name='die_refP')
        refMove = root.Set(referencePoints=(refPs[refP1.id],), name='move_refP')
        #interaction
        int1 = DieDraw.ContactProperty('Int-1')
        int1.TangentialBehavior(formulation=PENALTY, table=((
            fric, ), ), maximumElasticSlip=FRACTION, fraction=0.005)
        cont1 = DieDraw.SurfaceToSurfaceContactStd(name='Int-1', 
            createStepName='Initial', master=conM, slave=conS, sliding=FINITE, 
            enforcement=NODE_TO_SURFACE, interactionProperty='Int-1', 
            adjustMethod=OVERCLOSED)
        coup1 = DieDraw.Equation(name='Const-1', terms=((1.0, 'move', 2), 
            (-1.0, 'move_refP', 2)))
        rigi1 = DieDraw.RigidBody(name='Const-3', refPointRegion=refDie,
            surfaceRegion=conM)
        #Mesh
        sWire = pWire.edges
        edge1 = sWire.findAt(((Di/2.0, Di*Ratio/2.0, 0.0),),)
        edge2 = sWire.findAt(((Di/4.0, 0.0, 0.0),),)
        pWire.setMeshControls(regions=pWire.faces, elemShape=QUAD, 
            technique=STRUCTURED)
        DivL, DivH = 200, 12
        pWire.seedEdgeByNumber(edges=edge1, number=DivL, constraint=FIXED)
        pWire.seedEdgeByNumber(edges=edge2, number=DivH, constraint=FIXED)
        elemType1 = mesh.ElemType(elemCode=CAX4R)
        pWire.setElementType(regions=fSet, elemTypes=(elemType1, ))
        pWire.generateMesh()
        #loads BC
        BC1 = DieDraw.DisplacementBC(name='BC-1', createStepName='Initial', 
            region=refDie, u1=SET, u2=SET, ur3=SET, distributionType=UNIFORM)
        BC2 = DieDraw.DisplacementBC(name='BC-2', createStepName='Initial',
            region=refMove, u1=UNSET, u2=SET, ur3=UNSET, distributionType=UNIFORM)
        BC2.setValuesInStep(stepName='drawing', u2=-1.0*Disp)
        BC3 = DieDraw.DisplacementBC(name='BC-3', createStepName='Initial',
            region=AXISBC, u1=SET, u2=UNSET, ur3=UNSET, distributionType=UNIFORM)
        inpName='pass'+str(i+1)
        myJob = mdb.Job(name=inpName, model=modelName, resultsFormat=ODB,
            multiprocessingMode=DEFAULT, numCpus=4, numDomains=4)
        myJob.writeInput(consistencyChecking=OFF)
        if i==0:
            myJob.submit()
            myJob.waitForCompletion()
            odb = session.openOdb(name = inpName+'.odb')
            vp.setValues(displayedObject=odb)
            label = int(DivL/2)*(DivH+1)
            inst = odb.rootAssembly.instances['WIRE']
            node = inst.getNodeFromLabel(label=label)
            XX0 = node.coordinates[0]
            frame = odb.steps.values()[-1].frames[-1]
            fopU = frame.fieldOutputs['U']
            DispXX1 = fopU.getSubset(region=node).values[0].data[0]
            Di_init = (XX0 + DispXX1)*2.0
            DoRL.append(Di_init)
            odbpath = os.getcwd()
            oo = session.odbs[os.path.join(odbpath, inpName+'.odb')]
            xyList = session.xyDataListFromField(odb=oo, outputPosition=NODAL, 
                variable=(('RF', NODAL, ((COMPONENT, 'RF2'), )), ), 
                nodeSets=('MOVE_REFP', ))[0]
            DataF = zip(*xyList)[1]
            PeakF = min(DataF)
            forces = [item for item in DataF if abs((item/PeakF)-1.0)<0.1]
            Force_init = abs(sum(forces)/len(forces))
            ForceL.append(Force_init)
            leng = leng*(Di/Di_init)**2
            UnitEnergy = UnitEnergy + Force_init*leng
            oldJob = inpName
            odb.close()
        else:
            fold = open(inpName+'.inp','r')
            newName = inpName + '_Mapped'
            fnew = open(newName+'.inp','w')
            sold=fold.readlines()
            for s in sold:
                fnew.write(s)
                ss=s.split()
                if len(ss)>=2:
                    if (ss[0]=='*End')&(ss[1]=='Assembly'):
                        YY = DispL[-2]
                        trans = '0.0,' + str(YY) + ',0.0' + '\n'
                        fnew.write('*Map solution\n')
                        fnew.write(trans)
            fold.close()
            fnew.close()
            comd = 'abaqus job='+newName+' oldjob='+oldJob+' int cpus=6'
            output = os.popen(comd)
            print output.read()
            odb = session.openOdb(name = newName+'.odb')
            vp.setValues(displayedObject=odb)
            label = int(DivL/2)*(DivH+1)
            inst = odb.rootAssembly.instances['WIRE']
            node = inst.getNodeFromLabel(label=label)
            XX0 = node.coordinates[0]
            frame = odb.steps.values()[-1].frames[-1]
            fopU = frame.fieldOutputs['U']
            DispXX1 = fopU.getSubset(region=node).values[0].data[0]
            Di_init = (XX0 + DispXX1)*2.0
            DoRL.append(Di_init)
            odbpath = os.getcwd()
            oo = session.odbs[os.path.join(odbpath, newName+'.odb')]
            xyList = session.xyDataListFromField(odb=oo, outputPosition=NODAL, 
                variable=(('RF', NODAL, ((COMPONENT, 'RF2'), )), ), 
                nodeSets=('MOVE_REFP', ))[0]
            DataF = zip(*xyList)[1]
            PeakF = min(DataF)
            forces = [item for item in DataF if abs((item/PeakF)-1.0)<0.1]
            Force_init = abs(sum(forces)/len(forces))
            ForceL.append(Force_init)
            leng = leng*(Di/Di_init)**2
            UnitEnergy = UnitEnergy + Force_init*leng
            oldJob = newName
            if i==(Num-1):
                Ymid = Di*Ratio/2.0
                rads = Di/2.0
                pth = session.Path(name='Pth'+str(i), type=RADIAL, 
                    expression=((0, Ymid, 0), (0, Ymid, 1), (rads, Ymid, 0)), 
                    circleDefinition=ORIGIN_AXIS, numSegments=20, radialAngle=0,
                    startRadius=0, endRadius=CIRCLE_RADIUS)
                vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
                vp.odbDisplay.setPrimaryVariable(variableLabel='S', 
                    outputPosition=INTEGRATION_POINT, 
                    refinement=(COMPONENT, 'S22'), )
                S22 = session.XYDataFromPath(name='Data'+str(i), path=pth, 
                    includeIntersections=False, projectOntoMesh=False, 
                    pathStyle=PATH_POINTS,shape=UNDEFORMED,labelType=TRUE_DISTANCE)
                S22Data = zip(*S22.data)[1]
                Dwire = Di_init
            odb.close()
    
    return (Dwire, leng, UnitEnergy, S22Data)
    
if __name__=='__main__':

    sourceFile = 'model.xls'
    PKLResult = 'SeriesResult.pkl'
    Num = 9
    Di_s,Do_s,Rd_s = getDataFromExcel(sourceFile, Num)
    angles = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0]
    DwireL = []
    lengL = []
    EnergyL = []
    S22DataL = []
    angleL = []
    for angle in angles:
        Rd_s = [angle/180.0*pi for item in range(Num)]
        try:
            [Dwire, leng, UnitEnergy, S22Data] = wireDrawing(Di_s,Do_s,Rd_s)
            DwireL.append(Dwire)
            lengL.append(leng)
            EnergyL.append(UnitEnergy)
            S22DataL.append(S22Data)
            angleL.append(angle)
        finally:
            print 'error'
    record = open(PKLResult,'wb')
    pickle.dump(DwireL,record)
    pickle.dump(lengL,record)
    pickle.dump(EnergyL,record)
    pickle.dump(S22DataL,record)
    pickle.dump(angleL,record)
    record.close()