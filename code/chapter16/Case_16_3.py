# -*- coding: mbcs -*-
from odbAccess import *
from abaqusConstants import *
#==============block1=======================
o = session.openOdb(name='myJob.odb', readOnly=False)
a = o.rootAssembly
ns = a.nodeSets
es = a.elementSets
nsX = ns['SETX']
nsXnodes = nsX.nodes
print len(nsX.nodes)
print nsX.nodes[0][0].instanceName
print nsX.nodes[1][0].instanceName
print nsX.nodes[2][0].instanceName
o.close()
#==============block2=======================
o = session.openOdb(name='myJob.odb', readOnly=False)
instes = o.rootAssembly.instances
print instes
inst1 = instes['PART-1-1']
inst2 = instes['PART-1-2']
inst3 = instes['PART-2-1']
nodes1 = inst1.nodes[1:10]
nodes2 = inst2.nodes[1:10]
nodes3 = inst3.nodes[1:10]
setOnInstance = inst1.NodeSet(name='setOnInst1', nodes=nodes1)
setOnAssembly = o.rootAssembly.NodeSet(name='setOnAssembly', nodes=(nodes1,nodes2,nodes3))
o.close()
#==============block3=======================
o = session.openOdb(name='myJob.odb', readOnly=False)
setFromLabel = o.rootAssembly.NodeSetFromNodeLabels(name = 'setFromLabel', nodeLabels = (('PART-1-1', (1,3,5,7,9)),('PART-1-2',(1,3,5,7,9))))
o.close()
o = session.openOdb(name='myJob.odb', readOnly=False)
session.viewports['Viewport: 1'].setValues(displayedObject=o)
o.close()
#==============block4=======================
from textRepr import *#Ϊ��ʹ��prettyPrint()����
o = session.openOdb(name='myJob.odb', readOnly=False) 
session.viewports['Viewport: 1'].setValues(displayedObject=o)
steps = o.steps
print steps
step = steps['myStep1']

print len(frames)
f1 = frames[0] #��frames�б���ȡ��һ��OdbFrame����
f2 = step.getFrame(frameValue=0.0) #���ú������֡����Ϊ0.0��OdbFrame����
f1==f2
prettyPrint(f1) 
HR = step.historyRegions #HRΪ�ֿ�����
prettyPrint(HR[HR.keys()[0]])#��ӡ�ֿ�HR�е�һ��������Ϣ
#==============block5=======================
from textRepr import *#Ϊ��ʹ��prettyPrint()����
o = session.openOdb(name='myJob.odb', readOnly=False) 
session.viewports['Viewport: 1'].setValues(displayedObject=o)
steps = o.steps
frames = steps['myStep1'].frames
f1 = frames[-1]
fop = f1.fieldOutputs #���OdbFrame�����д洢����Ĳֿ�fieldOutput
prettyPrint(fop)#��ǰ�ֿ��д洢�������������λ�Ƴ�U��Ӧ����S
fopS = fop['S']#FieldOutput����Ӧ��������
fopU = fop['U']#FieldOutput����λ�Ƴ�����
prettyPrint(fopS.locations[0])#locationsΪ��¼�����������FieldLocation��������
prettyPrint(fopU.locations[0])
prettyPrint(fopS.values[0])#foS.valuesΪ����������ֵFieldValue��������
print fopS.values[0].mises
print fopS.values[0].magnitude
print fopU.values[0].magnitude
print fopU.values[0].mises
#==============block5=======================
setX=o.rootAssembly.nodeSets['SETX']
print len(setX.nodes[0])+len(setX.nodes[1])+len(setX.nodes[2])
fopUFromSet = fopU.getSubset(region=setX)#���SETX���ϴ��Ľ�����ݶ���
print len(fopUFromSet.values)
fopSFromSet = fopS.getSubset(region=setX)
print len(fopSFromSet.values)
setXE = o.rootAssembly.elementSets['SETX']
print len(setXE.elements[0])+len(setXE.elements[1])+len(setXE.elements[2])
fopSFromSet = fopS.getSubset(region=setXE)
print len(fopSFromSet.values)
inst1 = o.rootAssembly.instances['PART-1-1']
ele1 = inst1.getElementFromLabel(label=30)#ȡ��Part-1-1�б��Ϊ30�ĵ�Ԫ
fopSFromEle = fopS.getSubset(region=ele1)#�����һ����Ԫ�����ݽ��
prettyPrint(fopSFromEle.values[0])