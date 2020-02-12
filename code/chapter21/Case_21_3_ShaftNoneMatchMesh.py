# -*- coding: mbcs -*-
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *

a_s = 30.0#shaft a
b_s = 20.0#shaft b
d_s = 0.1#interference value
dL_b = 2.0#thickness of the sleeve at B end

Size = dL_b/4.0
NumP = 20
theta_base = [pi/2.0*i/NumP for i in range(0, NumP+1)]
#dL = lambda theta : dL_b + c1*theta + c2*theta**2 + c3*theta**3
#[c1, c2, c3] = [1.0, 0.0, 0.0]
dList = [dL_b for theta in theta_base]
x_shaft = [a_s*sin(theta) for theta in theta_base]
y_shaft = [b_s*cos(theta) for theta in theta_base]
xp_shaft = [(a_s-dL_b)*sin(theta) for theta in theta_base]
yp_shaft = [(b_s-dL_b)*cos(theta) for theta in theta_base]
x_sleevei = [(a_s-d_s)*sin(theta) for theta in theta_base]
y_sleevei = [(b_s-d_s)*cos(theta) for theta in theta_base]
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

theta_pick = [pi/2.0*(i+0.5)/NumP for i in range(0, NumP)]
pickShaft = [((a_s*sin(i), b_s*cos(i), 0),) for i in theta_pick]
pickSleeve = [(((a_s-d_s)*sin(i),(b_s-d_s)*cos(i),0),) for i in theta_pick]
modelName = 'RE'
inpName = 'RE_Result_Miss'
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
#Shaft.seedEdgeByNumber(edges=pEdges, number=4, constraint=FIXED)
eSleeve = Sleeve.edges
pEdges = eSleeve.findAt(*pickSleeve)
#Sleeve.seedEdgeByNumber(edges=pEdges, number=4, constraint=FIXED)
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
job = mdb.Job(name=inpName, model=modelName, numCpus=1)
job.submit(consistencyChecking=OFF)
job.waitForCompletion()
odb = session.openOdb(name=inpName+'.odb')
vp.setValues(displayedObject=odb)
vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
vp.odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=
    INTEGRATION_POINT, refinement=(INVARIANT, 'Max. Principal'), )
vp.odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, 
    visibleEdges=FREE, uniformScaleFactor=1)
vp.odbDisplay.contourOptions.setValues(spectrum='White to black')
vp.restore()
vp.setValues(width=100,height=80)
vp.view.fitView()
vp.viewportAnnotationOptions.setValues(state=OFF, annotations=OFF, 
    compass=OFF, legendBox=OFF, legendTitle=OFF, legendDecimalPlaces=1,
    legendNumberFormat=FIXED)
leaf = dgo.LeafFromPartInstance(partInstanceName=('SLEEVE-1', ))
vp.odbDisplay.displayGroup.replace(leaf=leaf)
