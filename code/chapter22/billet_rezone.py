"""
Reads the output database file and imports the deformed shape of
the billet at the end of step 1 as an orphan mesh part.  The
orphan mesh part is then used to create a 2D solid part which
can be meshed by the user.
"""
from abaqus import *
from abaqusConstants import *
import part

# NOTE:  USER MUST DEFINE THESE VARIABLES.
odbName = 'billet_case1_std_coarse.odb'      # Name of output database file.
modelName = 'Model-1'       # Model name.
orphanInstance = 'BILLET-1' # Deformed instance name.
deformedShape = DEFORMED    # Shape.
angle = 15.0                # Feature angle.
importStep = 0              # Step number.

# Import orphan mesh part.
orphanBillet = mdb.models['Model-1'].PartFromOdb(fileName=odbName,
                                                name='orphanBillet',
                                                instance=orphanInstance,
                                                shape=deformedShape,
                                                step=importStep)

# Extract 2D profile and create a solid part.
newBillet = mdb.models['Model-1'].Part2DGeomFrom2DMesh(name='newBillet',
                                                      part=orphanBillet,
                                                      featureAngle=angle)

print 'Deformed billet is now ready for rezoning.'
