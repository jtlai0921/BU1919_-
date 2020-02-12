# -*- coding: mbcs -*-
import csv, re
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbAccess import *
from pyGene4TankCAE.gene import FloatGene
from pyGene4TankCAE.organism import Organism
from pyGene4TankCAE.population import Population

# gene classes for rib positions

class OrgGene1(FloatGene):
    """
    gene to refer to the first rib position
    """
    mutProb = 0.2
    mutAmt = 0.5

    randMin = 8000.0/4.0
    randMax = 8000.0/2.0

class OrgGene2(FloatGene):
    """
    gene to refer to the distance between ribs
    """
    mutProb = 0.2
    mutAmt = 0.5

    randMin = 1000.0
    randMax = 4000.0

# organism class

class CAEOrganism(Organism):
    """
    organism class
    """
    genome = {}
    genome['a']=OrgGene1
    genome['b']=OrgGene2

    def fitness(self):
        """
        Best fitness is of the lowest buckling factor
        """
        inputList = self.getDataSet()
        result = 0.0
        if inputList[1]>6000.0:
            result = 100.0
        else:
            result = -1.0*performCAE(inputList)
        return result
        
    def getDataSet(self):
        """
        computes the input data from genes
        """
        avalue = float(self.genes['a'].value)
        bvalue = float(self.genes['b'].value)
        SPData = [avalue, avalue+bvalue]
        return SPData

class CAEPopulation(Population):

    species = CAEOrganism
    initPopulation = 36#20

    # cull to this many children after each generation
    childCull = 10#10

    # number of children to create after each generation
    childCount = 20#30

    # keep best parents    
    incest = 4

    # add random children
    numNewOrganisms = 5


def performCAE(poList):

    Hei = 8000.0
    Dwall = 1500.0
    Hwall = 10.0
    Lrib = 400.0
    Hrib = 10.0
    Prib = poList
    Psec = Prib + [Hei]
    Nrib = len(Psec)
    offList = []
    Pstart = 0.0
    for item in Psec:
        offList.append((item - Lrib/2.0 - Pstart)/2.0 + Lrib/2.0)
        Pstart = item + Lrib/2.0
    Press = 9800.0*1.0e-9*Hei
    inpName = 'Buck'
    Mdb()
    md = mdb.models['Model-1']
    #Part definition
    s1 = md.ConstrainedSketch(name='tank', sheetSize=200.0)
    s1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s1.Line(point1=(0.0, Hei), point2=(Dwall/2.0, Hei))
    s1.Line(point1=(Dwall/2.0, Hei), point2=(Dwall/2.0, 0.0))
    s1.Line(point1=(Dwall/2.0, 0.0), point2=(0.0, 0.0))
    pTank = md.Part(name='tank', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    pTank.BaseShellRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
    pPlane = []
    dat = pTank.datums
    for posi in Prib:
        idi = pTank.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, 
            offset=posi+Lrib/2.0).id
        fcs = pTank.faces
        pTank.PartitionFaceByDatumPlane(datumPlane=dat[idi], faces=fcs)
        idi = pTank.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, 
            offset=posi-Lrib/2.0).id
        fcs = pTank.faces
        pTank.PartitionFaceByDatumPlane(datumPlane=dat[idi], faces=fcs)
    #Materials and Sections
    MatP = md.Material(name='Plastic')
    MatP.Density(table=((1e-09, ), ))
    MatP.Elastic(table=((10000.0, 0.3), ))
    MatS = md.Material(name='steel')
    MatS.Density(table=((1e-09, ), ))
    MatS.Elastic(table=((200000.0, 0.3), ))
    md.HomogeneousShellSection(name='Section-wall', thickness=Hwall,
        preIntegrate=ON, material='Plastic', thicknessType=UNIFORM)
    md.HomogeneousShellSection(name='Section-rib', thickness=(Hwall+Hrib),
        preIntegrate=ON, material='Plastic', thicknessType=UNIFORM)
    md.HomogeneousShellSection(name='Section-cov', thickness=16.0,
        preIntegrate=ON, material='steel', thicknessType=UNIFORM)
    points = []
    fcs = pTank.faces
    for yi in Prib:
        points.append(((-Dwall/2.0, yi, 0.0),))
    faces = fcs.findAt(*points)
    ribSet = pTank.Set(name='ribs', faces=faces)
    pTank.SectionAssignment(region=ribSet, sectionName='Section-rib')
    points = []
    for (i, yi) in enumerate(Psec):
        points.append(((-Dwall/2.0, yi-offList[i], 0.0),))
    faces = fcs.findAt(*points)
    wallSet = pTank.Set(name='walls', faces=faces)
    pTank.SectionAssignment(region=wallSet, sectionName='Section-wall')
    faces = fcs.findAt(((0.0, 0.0, 0.0),),((0.0, Hei, 0.0),))
    covSet = pTank.Set(name='covers', faces=faces)
    pTank.SectionAssignment(region=covSet, sectionName='Section-cov')
    #Assembly
    root = md.rootAssembly
    inst = root.Instance(name='tank', part=pTank, dependent=ON)
    root.rotate(instanceList=('tank', ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(10.0, 0.0, 0.0), angle=90.0)
    #step and Load-BC
    md.BuckleStep(name='Buck', previous='Initial', numEigen=2, vectors=4,
        maxIterations=200)
    points = []
    for zi in Prib:
        points.append(((-Dwall/2.0, 0.0, zi),))
    for (i, zi) in enumerate(Psec):
        points.append(((-Dwall/2.0, 0.0, zi-offList[i]),))
    fcs = inst.faces
    faces1 = fcs.findAt(*points)
    hydroSur = root.Surface(name='hydroSur', side1Faces=faces1)
    faces2 = fcs.findAt(((0.0, 0.0, 0.0),),)
    fixSet = root.Set(name='fix', faces=faces2)
    md.EncastreBC(name='fix', createStepName='Buck', region=fixSet)
    md.Pressure(name='Hydro', createStepName='Buck', region=hydroSur, 
        distributionType=HYDROSTATIC, field='', magnitude=Press, 
        amplitude=UNSET, hZero=Hei, hReference=0.0)
    #Mesh
    pTank.seedPart(size=100.0, deviationFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=S3, elemLibrary=STANDARD)
    faces = pTank.faces
    AllFace = pTank.Set(name='AllFace', faces=faces)
    pTank.setElementType(regions=AllFace, elemTypes=(elemType1, elemType2))
    pTank.generateMesh()
    root.regenerate()
    job = mdb.Job(name=inpName, model='Model-1', numCpus=6, numDomains=6)
    #Job and sumbit
    try:
        job.submit(consistencyChecking=OFF)
        job.waitForCompletion()
        odb = session.openOdb(name=inpName+'.odb')
        step = odb.steps.values()[0]
        Descr = step.frames[1].description
        Result = float(re.split('= ', Descr)[-1])
    except BaseException, e:# in case fail to get result and set the default
        Result = 0.0

    return Result

# create an initial random population
p0 = [float(item) for item in range(1500, 4500, 500)]
d0 = [float(item) for item in range(1500, 4500, 500)]
oList = []
for p0i in p0:
    for d0i in d0:
        oList.append(CAEOrganism(*[p0i, d0i]))
pop = CAEPopulation(*oList)

# now a func to run the population
def main():
    i = 0
    outFile = csv.writer(file('out.csv', 'wb'))
    while i<40:
        # execute a generation
        pop.gen()
        best = pop.organisms[0]
        outStr = ['iter', str(i)]
        outFile.writerow(outStr)
        for org in pop.organisms:
            outStr = []
            [outStr.append(org.genes[key].value) for key in 'ab']
            outStr.append('fitness')
            outStr.append(org.fitnessValue)
            outFile.writerow(outStr)
        i+=1

if __name__ == '__main__':
    main()