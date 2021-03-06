"""
simpleMonitor.py

Print all messages issued during an ABAQUS solver 
analysis to the ABAQUS/CAE command line interface
"""

from abaqus import *
from abaqusConstants import *  
from jobMessage import ANY_JOB, ANY_MESSAGE_TYPE

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def simpleCB(jobName, messageType, data, userData):
    """
    This callback prints out all the
    members of the data objects
    """

    format = '%-18s  %-18s  %s'
    
    print 'Message type: %s'%(messageType)
    print
    print 'data members:'
    print format%('member', 'type', 'value')
    
    members =  dir(data)
    for member in members:
        if member.startswith('__'): continue # ignore "magic" attrs
        memberValue = getattr(data, member)
        memberType = type(memberValue).__name__
        print format%(member, memberType, memberValue)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def printMessages(start=ON):
    """
    Switch message printing ON or OFF
    """
    
    if start:
        monitorManager.addMessageCallback(ANY_JOB, 
            ANY_MESSAGE_TYPE, simpleCB, None)
    else:
        monitorManager.removeMessageCallback(ANY_JOB, 
            ANY_MESSAGE_TYPE, simpleCB, None)

