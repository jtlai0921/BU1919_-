# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *  
from jobMessage import JOB_ABORTED, JOB_COMPLETED, JOB_SUBMITTED
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dealResult(jobName, messageType, data, userData):
    import winsound
    import visualization
    if ((messageType==JOB_ABORTED) or (messageType==JOB_SUBMITTED)):
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    elif (messageType==JOB_COMPLETED):
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        odb = visualization.openOdb(path=jobName + '.odb')
        userData.setValues(displayedObject=odb)
        userData.odbDisplay.display.setValues(plotState=CONTOURS_ON_DEF)