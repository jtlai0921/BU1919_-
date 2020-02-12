# RPCreatorDB.py
from abaqusGui import *
from abaqusConstants import *
from symbolicConstants import *

###########################################################################
# DB Class definition
###########################################################################

class RPCreatorDB(AFXDataDialog):
    def __init__(self, procedure):
        self.procedure = procedure
        AFXDataDialog.__init__(self, self.procedure, 'Select Position',
            self.OK|self.CONTINUE|self.CANCEL, opts=LAYOUT_FIX_WIDTH|\
            LAYOUT_FIX_HEIGHT|DATADIALOG_BAILOUT|\
            DIALOG_ACTIONS_SEPARATOR )
        AFXTextField(p=self,ncols=15,
            labelText='INPUT Coordinate otherwise press continue:',
            tgt=self.procedure.coordKw,sel=0, opts=AFXTEXTFIELD_STRING )