# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
#==============Sketch: Revolve=======================
if mdb.models.has_key('myModel'):
    m = mdb.models['myModel']
else:
    m = mdb.Model(name='myModel')
Sr = m.ConstrainedSketch(name='Revolve', sheetSize=200.0)
g = Sr.geometry
Sr.setPrimaryObject(option=SUPERIMPOSE)
cline = Sr.ConstructionLine((0,20), (0,-20))
Sr.assignCenterline(line=cline)
line1 = Sr.Line(point1=(0.0, 15.0), point2=(15.0, 15.0))
line2 = Sr.Line(point1=(15.0, 15.0), point2=(15.0, 0.0))
line3 = Sr.Line(point1=(15.0, 0.0), point2=(0.0, 0.0))
line4 = Sr.Line(point1=(5.0,0.0), point2=(5.0,15.0))
Sr.autoTrimCurve(curve1=line1, point1=(0.0, 15.0))
Sr.autoTrimCurve(curve1=line3, point1=(0.0, 0.0))
Sr.unsetPrimaryObject()
#==============Sketch: Extrude=======================
Se = m.ConstrainedSketch(name='Extrude', sheetSize=200.0)
g, c = Se.geometry, Se.constraints
Se.setPrimaryObject(option=STANDALONE)
line1 = Se.Line(point1=(0.0, 15.0), point2=(15.0, 15.0))
line2 = Se.Line(point1=(15.0, 15.0), point2=(15.0, 0.0))
line3 = Se.Line(point1=(15.0, 0.0), point2=(0.0, 0.0))
line4 = Se.Line(point1=(0.0,0.0), point2=(0.0,15.0))
Se.PerpendicularConstraint(entity1=line3, entity2=line4)
Se.autoDimension(objectList=(line4,))
Se.unsetPrimaryObject()
#==============Part Create Step=======================
p1 = mdb.models['myModel'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p1.BaseSolidExtrude(sketch=Se, depth=20.0)
p2 = mdb.models['myModel'].Part(name='Part-2', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p2.BaseSolidRevolve(sketch=Sr, angle=90.0, flipRevolveDirection=OFF)
#==============Material: Definition=======================
mdb.models['myModel'].Material(name='Steel')
mdb.models['myModel'].materials['Steel'].Density(table=((7.8e-09, ), ))
mdb.models['myModel'].materials['Steel'].Elastic(table=((210000.0, 0.28), ))
mdb.models['myModel'].materials['Steel'].Plastic(table=((450.0, 0.0), (480.0, 
    0.05), (490.0, 0.15), (500.0, 0.3)))
mdb.models['myModel'].materials['Steel'].Expansion(table=((1e-05, ), ))
mdb.models['myModel'].HomogeneousSolidSection(name='Section-Steel', 
    material='Steel', thickness=None)
c1 = p1.cells
region1 = regionToolset.Region(cells=c1)
p1.SectionAssignment(region=region1, sectionName='Section-Steel', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
c2 = p2.cells
region2 = regionToolset.Region(cells=c2)
p2.SectionAssignment(region=region2, sectionName='Section-Steel', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
#==============Assembly: Definition=======================
a = mdb.models['myModel'].rootAssembly
p11 = a.Instance(name='Part-1-1', part=p1, dependent=ON)
p12 = a.Instance(name='Part-1-2', part=p1, dependent=ON)
p21 = a.Instance(name='Part-2-1', part=p2, dependent=ON)
#a.translate(instanceList=('Part-1-1', ), vector=(0.0, 15.0, 0.0))
#a.translate(instanceList=('Part-1-2', ), vector=(0.0, -15.0, 0.0))
p11.translate(vector=(0.0, 15.0, 0.0))
p12.translate(vector=(0.0, -15.0, 0.0))
#==============Step: Definition=======================
mdb.models['myModel'].StaticStep(name='myStep1', previous='Initial', 
    maxNumInc=1000, initialInc=0.1, minInc=0.001, maxInc=0.3, nlgeom=ON)
FRes = mdb.models['myModel'].fieldOutputRequests
FRes[FRes.keys()[0]].setValues(numIntervals=10, variables=('S', 'U'))
#==============Contact&Load: Definition=======================
mdb.models['myModel'].ContactProperty('IntProp-1')
mdb.models['myModel'].interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models['myModel'].ContactStd(name='Int-1', createStepName='Initial')
mdb.models['myModel'].interactions['Int-1'].includedPairs.setValuesInStep(
    stepName='Initial', useAllstar=ON)
mdb.models['myModel'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
    stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp-1'), ))
#: The interaction "Int-1" has been created.

f12 = p12.faces
f11 = p11.faces
f21 = p21.faces
f1x = f12.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
f2x = f11.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
f3x = f21.getByBoundingBox(xMin=-1, xMax=1, yMin=-20, yMax=40, zMin=-1, zMax=25)
setX = a.Set(name='setX', faces=f1x+f2x+f3x)
surfaceX = a.Surface(name='surfaceX', side1Faces=f1x+f2x+f3x)
regionX = regionToolset.Region(faces=f1x+f2x+f3x)
f1z = f12.getByBoundingBox(zMin=-1, zMax=1, yMin=-20, yMax=40, xMin=-1, xMax=25)
f2z = f11.getByBoundingBox(zMin=-1, zMax=1, yMin=-20, yMax=40, xMin=-1, xMax=25)
f3z = f21.getByBoundingBox(zMin=-1, zMax=1, yMin=-20, yMax=40, xMin=-1, xMax=25)
setZ = a.Set(name='setZ', faces=f1z+f2z+f3z)
regionZ = regionToolset.Region(faces=f1z+f2z+f3z)
f4 = f12.getByBoundingBox(xMin=-1, xMax=25, yMin=-20, yMax=-10, zMin=-1, zMax=25)
regionY = regionToolset.Region(faces=f4)
f5 = f11.getByBoundingBox(xMin=-1, xMax=25, yMin=25, yMax=40, zMin=-1, zMax=25)
regionYP = regionToolset.Region(side1Faces=f5)

mdb.models['myModel'].XsymmBC(name='BC-X', createStepName='Initial', 
    region=regionX)
mdb.models['myModel'].ZsymmBC(name='BC-Z', createStepName='Initial', 
    region=regionZ)
mdb.models['myModel'].DisplacementBC(name='BC-YFix', createStepName='Initial', 
    region=regionY, u1=UNSET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
mdb.models['myModel'].Pressure(name='Pressure', createStepName='myStep1', 
    region=regionYP, distributionType=UNIFORM, field='', magnitude=10.0, 
    amplitude=UNSET)
#==============Mesh: Definition=======================
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
p1.seedPart(size=1.5, deviationFactor=0.1)
c1 = p1.cells
p1.setElementType(regions=(c1,), elemTypes=(elemType1, ))
p1.generateMesh()
p2.seedPart(size=1.5, deviationFactor=0.1)
c2 = p2.cells
p2.setMeshControls(regions=c2, technique=SWEEP, algorithm=ADVANCING_FRONT)
p2.setElementType(regions=(c2,), elemTypes=(elemType1, ))
p2.generateMesh()
a.regenerate()
#==============Job: Definition=======================
mdb.Job(name='myJob', model='myModel', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=50, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=1)
#==============Job: Excecution=======================
mdb.jobs['myJob'].submit()
mdb.jobs['myJob'].waitForCompletion()
import winsound
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)