# file: showIndex_plugin.py
from abaqusGui import *
from abaqusConstants import *
from symbolicConstants import *
from RPCreator_DB import RPCreatorDB

class RPCreatorProcedure(AFXProcedure):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        # Construct the base class.
        AFXProcedure.__init__(self, owner)
        self.cmd = AFXGuiCommand(self, 'RPCreator', 'RPCreator_kernel', True)
        self.pickedEntityKw = AFXObjectKeyword( self.cmd, 'pickedEntity',
            isRequired=False, defaultValue='')
        self.coordKw = AFXTupleKeyword( self.cmd, 'coord', isRequired=False,
            minLength=3, maxLength=3)

    def getFirstStep(self):
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.pickedEntityKw.setValueToDefault(True)
        db = RPCreatorDB(self)
        self.step1 = AFXDialogStep(self, db, "Specify Input")
        prompt = "Plz select a vertex to creat reference point..."
        self.step2 = AFXPickStep(owner=self, keyword=self.pickedEntityKw,
            prompt=prompt, entitiesToPick=VERTICES|INTERESTING_POINTS|DATUM_POINTS)
        return self.step1

    def getNextStep(self, previousStep):
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if (previousStep == self.step1):
            return self.step2
        elif (previousStep == self.step2):
            return None

#####################################################

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# Register a GUI plug-in in the Plug-ins menu.
toolset.registerGuiMenuButton(
    object=RPCreatorProcedure(toolset), buttonText='RPCreator...',
    version='1.0', author='JingheSu@gmail.com',
    applicableModules =  ['Part','Assembly'],
    kernelInitString = 'import RPCreator_kernel',
    description='Creat reference point'
    )
