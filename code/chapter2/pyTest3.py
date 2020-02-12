# -*- coding: utf-8 -*-

from abaqus import *
from abaqusConstants import *
from viewerModules import *
import regionToolset
import mesh

length = 1000 #mm
Cload = 40 #N
radius = 3.0 #mm
Mdb()
#: Create a mdb: model-1.
s = mdb.models['Model-1'].ConstrainedSketch(name='beam', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.Line(point1=(0.0, 0.0), point2=(length, 0.0))
p = mdb.models['Model-1'].Part(name='beam', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['beam']
p.BaseWire(sketch=s)
del mdb.models['Model-1'].sketches['beam']

mdb.models['Model-1'].Material(name='steel')
mdb.models['Model-1'].materials['steel'].Elastic(table=((210000.0, 0.28), ))
mdb.models['Model-1'].materials['steel'].Density(table=((7.8e-09, ), ))
mdb.models['Model-1'].CircularProfile(name='Profile-1', r=radius)
mdb.models['Model-1'].BeamSection(name='Section-beam', profile='Profile-1', 
    integration=DURING_ANALYSIS, poissonRatio=0.28, material='steel', 
    temperatureVar=LINEAR)
p = mdb.models['Model-1'].parts['beam']
e = p.edges
region = regionToolset.Region(edges=e)
p.SectionAssignment(region=region, sectionName='Section-beam', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
e = p.edges
region=regionToolset.Region(edges=e)
p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, 
    -1.0))

a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['beam']
a.Instance(name='beam-1', part=p, dependent=ON)

mdb.models['Model-1'].StaticStep(name='Step-load', previous='Initial', 
    nlgeom=ON)

a = mdb.models['Model-1'].rootAssembly
v1 = a.instances['beam-1'].vertices
verts1 = v1.findAt(((0,0,0),),)
a.Set(vertices=verts1, name='Set-fix')
verts1 = v1.findAt(((length,0,0),),)
a.Set(vertices=verts1, name='Set-force')
region = a.sets['Set-fix']
mdb.models['Model-1'].DisplacementBC(name='BC-fix', createStepName='Step-load', 
    region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
region = a.sets['Set-force']
mdb.models['Model-1'].ConcentratedForce(name='Load-load', 
    createStepName='Step-load', region=region, cf2=-1.0*Cload, 
    distributionType=UNIFORM, field='', localCsys=None)

p = mdb.models['Model-1'].parts['beam']
e = p.edges
p.seedEdgeBySize(edges=e, size=length/100.0, deviationFactor=0.1, 
    constraint=FINER)
elemType1 = mesh.ElemType(elemCode=B32, elemLibrary=STANDARD)
pickedRegions =(e, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))
p.generateMesh()
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
mdb.Job(name='beam-load', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=50, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['beam-load'].submit(consistencyChecking=OFF)

mdb.jobs['beam-load'].waitForCompletion()
odbpath = os.path.join(os.getcwd(),"beam-load.odb")
pngPath = os.path.join(os.getcwd(),"deformation")
oo = session.openOdb(name=odbpath)
vp = session.Viewport(name='myView')
vp.makeCurrent()
vp.maximize()
vp.setValues(displayedObject=oo)
vp.odbDisplay.setPrimaryVariable(variableLabel='U', 
    outputPosition=NODAL, refinement=(INVARIANT, 'Magnitude'), )
vp.odbDisplay.display.setValues(plotState=CONTOURS_ON_DEF)
session.graphicsOptions.setValues(backgroundStyle=SOLID, 
    backgroundColor='#FFFFFF')
vp.viewportAnnotationOptions.setValues(legendDecimalPlaces=2, 
    legendNumberFormat=SCIENTIFIC, triad=OFF, legendBox=OFF)
vp.viewportAnnotationOptions.setValues(
    legendFont='-*-verdana-medium-r-normal-*-*-180-*-*-p-*-*-*')
vp.viewportAnnotationOptions.setValues(
    legendFont='-*-verdana-bold-r-normal-*-*-180-*-*-p-*-*-*')
vp.odbDisplay.contourOptions.setValues(spectrum='Black to white')
vp.viewportAnnotationOptions.setValues(
    titleFont='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
vp.viewportAnnotationOptions.setValues(
    stateFont='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
vp.view.fitView()
session.printOptions.setValues(vpDecorations=OFF, reduceColors=False)
session.printToFile(fileName=pngPath, format=TIFF, canvasObjects=(
    vp, ))

