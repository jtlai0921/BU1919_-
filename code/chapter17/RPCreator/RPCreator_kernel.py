# RPCreator_kernel.py
from abaqus import *
from abaqusConstants import *
from symbolicConstants import *

def RPCreator(coord=(), pickedEntity=None):
    # Create Reference Point
    cObject = getCurrentDisplayObject()
    rp = None
    if len(coord)==3:
        rp = cObject.ReferencePoint(coord)
    else:
        rp = cObject.ReferencePoint(pickedEntity)
    cObject.regenerate()
    print 'New Reference point created!'
    return rp

def getCurrentDisplayObject():
    # Get current object: part or assembly
    vpName = session.currentViewportName
    CObject = session.viewports[vpName].displayedObject
    return CObject