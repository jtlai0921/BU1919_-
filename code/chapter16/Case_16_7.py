# -*- coding: mbcs -*-
from math import *
from odbAccess import *
from abaqusConstants import *
name = 'BeamADeform'
path = 'BeamADeform.odb'
R = 50.0
fN=6
Num = 2**fN*50

o = Odb(name=name, path=path)
part = o.Part(name='beam', embeddedSpace=THREE_D, type=DEFORMABLE_BODY)
nodeLabels = range(1, Num+1)
xNode = [R*sin((node-1.0)/Num*2.0*pi) for node in nodeLabels]
yNode = [R*cos((node-1.0)/Num*2.0*pi) for node in nodeLabels]
zNode = [0.0 for node in nodeLabels]
nodeData = zip(nodeLabels, xNode, yNode, zNode)
part.addNodes(nodeData=nodeData, nodeSetName='beamPart')
nodelist1 = range(1, Num+1)
nodelist2 = [node+1 if node<Num else 1 for node in nodelist1]
eleLabels = range(1, Num+1)
eleData = zip(eleLabels, nodelist1, nodelist2)
part.addElements(elementData=eleData, type='B31')
inst = o.rootAssembly.Instance(name='beamInstance', object=part)
step = o.Step(name='deform', description='Step4Deform', domain=TIME,
    timePeriod=1.0)
for i in range(fN):
    dataU, dataS = [], []
    base = Num/2**i
    for m in nodeLabels:
        temp = m%base/float(base)*pi + m/base*2.0*pi
        dataU.append((0.0,0.0,5.0*sin(temp)*i))
        dataS.append((5.0*sin(temp)*i,0.0,0.0))
    frame = step.Frame(incrementNumber=i, frameValue=float(i)/(fN-1),
        description='Step time: '+str(float(i)/(fN-1)))
    fopU = frame.FieldOutput(name='U', description='Custom data', type=VECTOR,
        validInvariants=(MAGNITUDE,))
    fopU.addData(position=NODAL, instance=inst, labels=nodeLabels,data=dataU)
    fopS = frame.FieldOutput(name='S', description='Custom data',
        type=TENSOR_3D_SURFACE, validInvariants=(MISES,))
    fopS.addData(position=INTEGRATION_POINT, instance=inst, labels=eleLabels,
        data=dataS)
o.save()
o.close()