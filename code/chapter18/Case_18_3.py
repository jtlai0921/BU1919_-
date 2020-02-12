# -*- coding: mbcs -*-
import pickle
import numpy as np
from abaqus import *
from abaqusConstants import *
from caeModules import *
from jobMessage import JOB_COMPLETED
from getShape import getShape
############################
length = 10000.0#mm
weight = 1.0#ton
pointA = (0.0, 0.0)#Final position of PointA
pointB = (5000.0, -1000.0)#Final position of PointB

area = [0.1, 0.3, 1.0]#mm^2
dens = [weight/length/areai for areai in area]
modulus = 200000.0
pointC = (length, 0.0)
Mvec = (pointB[0]-pointC[0], pointB[1]-pointC[1])
Gravity = 9800.0
preDisp = 50.0
Results = open('data.pkl', 'wb')
#############################
ropeMdb = Mdb(pathName='HangingChain.cae')
for (i, areai) in enumerate(area):
    modelName = 'TrussModelS'+str(i)
    m = ropeMdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)
    #Create Part
    s = m.ConstrainedSketch(name='Truss', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    line1 = s.Line(point1=pointA, point2=pointC)
    s.HorizontalConstraint(entity=line1)
    p = ropeMdb.models[modelName].Part(name='rope', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
    p.BaseWire(sketch=s)
    #Material and Section
    ropeMdb.models[modelName].Material(name='Material-Steel')
    ropeMdb.models[modelName].materials['Material-Steel'].Density(
        table=((dens[i], ), ))
    ropeMdb.models[modelName].materials['Material-Steel'].Elastic(
        table=((modulus, 0.3), ))
    ropeMdb.models[modelName].TrussSection(name='Section-Truss', 
        material='Material-Steel', area=areai)
    e = p.edges
    setPart = p.Set(name='set4Section', edges=e)
    p.SectionAssignment(region=setPart, sectionName='Section-Truss',
        offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    # Assembly and sets
    a = ropeMdb.models[modelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    inst = a.Instance(name='theRope', part=p, dependent=ON)
    v = inst.vertices
    verts1 = v.findAt(((pointA[0],pointA[1],0.0),),)
    setFix = a.Set(vertices=verts1, name='Set4Fix')
    verts2 = v.findAt(((pointC[0],pointC[1],0.0),),)
    setMove = a.Set(vertices=verts2, name='Set4Move')
    e = inst.edges
    setGravity = a.Set(edges=e, name='Set4Gravity')
    #Steps and Loads
    ropeMdb.models[modelName].StaticStep(name='Step-PreTension', 
        previous='Initial', initialInc=0.01, minInc=0.0001, nlgeom=ON)
    ropeMdb.models[modelName].StaticStep(name='Step-Gravity', 
        previous='Step-PreTension', minInc=0.001, initialInc=0.2)
    ropeMdb.models[modelName].StaticStep(name='Step-StressRelease', 
        previous='Step-Gravity', initialInc=0.01, minInc=0.001)
    ropeMdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(
        variables=('S', 'LE', 'U'))
    Load = ropeMdb.models[modelName].Gravity(name='Load-Gravity', 
        createStepName='Step-Gravity', comp2=-1.0*Gravity, field='', 
        distributionType=UNIFORM, region=setGravity)
    BC1 = ropeMdb.models[modelName].DisplacementBC(name='BC-Fix', region=setFix,
        createStepName='Step-PreTension', u1=0.0, u2=0.0, ur3=UNSET,
        amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    BC2 = ropeMdb.models[modelName].DisplacementBC(name='BC-Move', fieldName='',
        createStepName='Step-PreTension', u1=preDisp, u2=0.0, ur3=UNSET, 
        amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, region=setMove,
        localCsys=None)
    BC2.setValuesInStep(stepName='Step-StressRelease', u1=Mvec[0], 
        u2=Mvec[1])
    # Generate Mesh
    p = ropeMdb.models[modelName].parts['rope']
    e = p.edges
    p.seedEdgeByNumber(edges=e, number=100, constraint=FINER)
    elemType1 = mesh.ElemType(elemCode=T2D2, elemLibrary=STANDARD)
    p.setElementType(regions=setPart, elemTypes=(elemType1, ))
    p.generateMesh()
    a = ropeMdb.models[modelName].rootAssembly
    a.regenerate()
    #Job and submit
    jobName = 'HangingChainTrussS'+str(i)
    curJob = ropeMdb.Job(name=jobName, model=modelName, description='',
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
        memory=50, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
        scratch='', multiprocessingMode=DEFAULT, numCpus=1)
    curJob.submit(consistencyChecking=OFF)
    curJob.waitForCompletion()
    ms = curJob.messages[-1]
    if ms.type==JOB_COMPLETED:
        odbPath = jobName+'.odb'
        instName, stepName = 'THEROPE', 'Step-StressRelease'
        xa, ya = getShape(odbPath, instName, stepName)
        stiff = areai*modulus
        label = r'$FEA: stiff= %i$'%stiff
        pickle.dump([xa, ya, label], Results)
Results.close()