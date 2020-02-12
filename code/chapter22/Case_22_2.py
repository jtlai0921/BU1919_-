# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *

#from abaqusConstants import *
#odb = session.openOdb('Data4Transfer.odb')
#p = mdb.models['Model-1'].PartFromOdb(name='part', instance='SPECIMAN', 
#    odb=odb, shape=DEFORMED, step=0, frame=10)

from abaqusConstants import *
copyMdb = mdb.Model(name='copyModel', objectToCopy=myModel)
copyMdb.materials['Alu'].Density(table=((2.7e-09, ), ))
copyMdb.materials['steel'].Density(table=((7.9e-09, ), ))
copyMdb.ExplicitDynamicsStep(name='Step-1', previous='Initial', 
    maintainAttributes=True, timePeriod=0.0001)
copyMdb.fieldOutputRequests['F-Output-1'].setValues(numIntervals=2)
instances = copyMdb.rootAssembly.instances.values()
copyMdb.InitialState(fileName='Data4Transfer', endStep=1, endIncrement=20,
    name='PreField', createStepName='Initial', instances=instances)
job = mdb.Job(name='DataTransfer', model='copyModel', type=ANALYSIS, 
    parallelizationMethodExplicit=DOMAIN, numDomains=1, 
    multiprocessingMode=DEFAULT, numCpus=1)
#updateReferenceConfiguration=ON, 