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
from textRepr import *#为了使用prettyPrint()函数
o = session.openOdb(name='myJob.odb', readOnly=False) 
session.viewports['Viewport: 1'].setValues(displayedObject=o)
steps = o.steps
print steps
step = steps['myStep1']

print len(frames)
f1 = frames[0] #从frames列表中取第一个OdbFrame对象
f2 = step.getFrame(frameValue=0.0) #利用函数获得帧特征为0.0的OdbFrame对象
f1==f2
prettyPrint(f1) 
HR = step.historyRegions #HR为仓库类型
prettyPrint(HR[HR.keys()[0]])#打印仓库HR中第一个对象信息
#==============block5=======================
from textRepr import *#为了使用prettyPrint()函数
o = session.openOdb(name='myJob.odb', readOnly=False) 
session.viewports['Viewport: 1'].setValues(displayedObject=o)
steps = o.steps
frames = steps['myStep1'].frames
f1 = frames[-1]
fop = f1.fieldOutputs #获得OdbFrame对象中存储结果的仓库fieldOutput
prettyPrint(fop)#当前仓库中存储的两类输出量：位移场U和应力场S
fopS = fop['S']#FieldOutput对象应力场变量
fopU = fop['U']#FieldOutput对象位移场变量
prettyPrint(fopS.locations[0])#locations为记录数据依附点的FieldLocation对象序列
prettyPrint(fopU.locations[0])
prettyPrint(fopS.values[0])#foS.values为场变量数据值FieldValue对象序列
print fopS.values[0].mises
print fopS.values[0].magnitude
print fopU.values[0].magnitude
print fopU.values[0].mises
#==============block5=======================
setX=o.rootAssembly.nodeSets['SETX']
print len(setX.nodes[0])+len(setX.nodes[1])+len(setX.nodes[2])
fopUFromSet = fopU.getSubset(region=setX)#获得SETX集合处的结果数据对象
print len(fopUFromSet.values)
fopSFromSet = fopS.getSubset(region=setX)
print len(fopSFromSet.values)
setXE = o.rootAssembly.elementSets['SETX']
print len(setXE.elements[0])+len(setXE.elements[1])+len(setXE.elements[2])
fopSFromSet = fopS.getSubset(region=setXE)
print len(fopSFromSet.values)
inst1 = o.rootAssembly.instances['PART-1-1']
ele1 = inst1.getElementFromLabel(label=30)#取得Part-1-1中编号为30的单元
fopSFromEle = fopS.getSubset(region=ele1)#获得这一个单元的数据结果
prettyPrint(fopSFromEle.values[0])