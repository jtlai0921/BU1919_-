# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *

def ODBPrinter (odbPath, variable, PngName, wid, heig):
    from odbAccess import *
    import os.path
    filePath = os.path.dirname(odbPath)
    PngPath = os.path.join(filePath, PngName)
    o = session.openOdb(name=odbPath)
    myViewport = session.viewports['Viewport: 1']
    myViewport.restore()
    myViewport.setValues(displayedObject=o, width=wid, height=heig)
    if variable=='S':
        myViewport.odbDisplay.setPrimaryVariable(variableLabel='S',
            outputPosition=INTEGRATION_POINT,refinement=(INVARIANT, 'Mises'))
    elif variable=='U':
        myViewport.odbDisplay.setPrimaryVariable(variableLabel='U',
            outputPosition=NODAL,refinement=(INVARIANT, 'Magnitude'))
    myViewport.odbDisplay.display.setValues(plotState=CONTOURS_ON_DEF)
    session.printOptions.setValues(vpDecorations=OFF, reduceColors=False)
    session.printToFile(fileName=PngPath, format=PNG,
        canvasObjects=(myViewport, ))
    o.close()
if __name__=='__main__':
    ODBPrinter('Test.odb', 'S', 'xxxx', 120, 80)