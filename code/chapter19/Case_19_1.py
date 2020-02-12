# -*- coding: mbcs -*-
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbAccess import *

wireR=1.0#
SpringR=15.0#
NN=8
GapR=0.3
angle=5.0#degree
Spitch=wireR*(2.0+GapR)/cos(angle/180.0*pi)#
Num=60
DR=wireR+SpringR
RatioRr=SpringR/wireR
da=2.0*pi/Num
dy=Spitch/Num
nodefileName='BeamSpringRr'+str(int(RatioRr))+'_node.inp'
elemfileName='BeamSpringRr'+str(int(RatioRr))+'_elem.inp'
setfileName='BeamSpringRr'+str(int(RatioRr))+'_set.inp'
inpfileName='BeamSpringRr'+str(int(RatioRr))+'_inp.inp'
jobName='BeamSpringRr'+str(int(RatioRr))+'_Spring'
NodeFile=open(nodefileName,'w')
ElemFile=open(elemfileName,'w')
SetFile=open(setfileName,'w')
InpFile=open(inpfileName,'w')
initN=0
initJ=(NN+1)*Num+10
x0=DR*cos(initN*da)
y0=initN*dy
z0=DR*sin(initN*da)
## form the node and element file
NodeFile.writelines('*NODE'+'\n')
NodeFile.writelines(str(initN+1)+', '+str(x0)+', '+str(y0)+', '+str(z0)+'\n')
ElemFile.writelines('*ELEMENT,'+' TYPE=B31,'+' ELSET=spring'+'\n')
while initN<=(Num*(NN+1)):
    initN=initN+1
    initJ=initJ+1
    x1=DR*cos(initN*da)
    y1=initN*dy
    z1=DR*sin(initN*da)
    xm=0.0
    ym=(initN+0.5)*dy
    zm=0.0
    NodeFile.writelines(str(initN+1)+', '+str(x1)+', '+str(y1)+', ' + 
        str(z1)+'\n')
    NodeFile.writelines(str(initJ)+', '+str(xm)+', '+str(ym)+', ' + 
        str(zm)+'\n')
    ElemFile.writelines(str(initN)+', '+str(initN)+', '+str(initN+1)+', ' + 
        str(initJ)+'\n')
#add the RP node
xp=0.0
yp=0.0
zp=0.0
NodeFile.writelines(str(Num*(NN+1)+6)+', '+str(xp)+', '+str(yp)+', ' + 
    str(zp)+'\n')
xp=0.0
yp=(NN+1)*Num*dy
zp=0.0
NodeFile.writelines(str(Num*(NN+1)+8)+', '+str(xp)+', '+str(yp)+', ' + 
    str(zp)+'\n')
NodeFile.close()
ElemFile.close()
## form the Set file
SetFile.writelines('*Beam Section, elset=spring, material=STEEL, poisson ' +
    '= 0.3, temperature=GRADIENTS, section=CIRC'+'\n')
SetFile.writelines(str(float(wireR))+'\n')
SetFile.writelines('*Nset, nset=Set-fix, generate'+'\n')
SetFile.writelines('1'+', '+str(1*Num/2+1)+', 1'+'\n')
SetFile.writelines('*Nset, nset=Set-twist, generate'+'\n')
SetFile.writelines(str(int((NN+0.5)*Num+1))+', '+str((NN+1)*Num+1)+', 1'+'\n')
SetFile.writelines('*Nset, nset=Set-fixRP'+'\n')
SetFile.writelines(str(Num*(NN+1)+6)+',\n')
SetFile.writelines('*Nset, nset=Set-twistRP'+'\n')
SetFile.writelines(str(Num*(NN+1)+8)+',\n')
SetFile.close()
## form the inp file
InpFile.writelines('*Heading'+'\n')
InpFile.writelines('** Generated by: Su Jinghe: alwjybai@gmail.com'+'\n')
InpFile.writelines('** -----------------------------------------------'+'\n')
InpFile.writelines('*INCLUDE, INPUT='+nodefileName+'\n')
InpFile.writelines('*INCLUDE, INPUT='+elemfileName+'\n')
InpFile.writelines('*INCLUDE, INPUT='+setfileName+'\n')
InpFile.writelines('*INCLUDE, INPUT=LoadandStep.inp'+'\n')
InpFile.close()
## submit the job and return the result
Mdb()
mdb.models['Model-1'].setValues(noPartsInputFile=ON)
mdb.JobFromInputFile(name=jobName,inputFileName=inpfileName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()
odbPath=jobName+'.odb'
odb = openOdb(odbPath)
nset = odb.rootAssembly.nodeSets['CONSTRAINT-TWIST_REFERNCE_POINT']
frame=odb.steps.values()[-1].frames[-1]
foutput=frame.fieldOutputs['RM']
fvalues=foutput.getSubset(region=nset).values[0].data[1]
odb.close()
print fvalues