# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *

def getByFeature (source, tol=1e-3, **arg):
    result, eSize, eRad, fSize ={},[],[],[]
    if arg.has_key('length'):
        length = arg['length']
        for e in source.edges:
            if abs(e.getSize()-length)<tol:
                eSize.append(e)
    if arg.has_key('radius'):
        radius = arg['radius']
        for e in source.edges:
            try:
                if abs(e.getRadius()-radius)<tol:
                    eRad.append(e)
            except Exception as e:
                print e
    if arg.has_key('area'):
        area = arg['area']
        for f in source.faces:
            if abs(f.getSize()-area)<tol:
                fSize.append(f)
    result['EdgeFromLength']=eSize;
    result['EdgeFromRadius']=eRad;
    result['FaceFromArea']=fSize;
    return result

if __name__=="__main__":
    try:#打开在当前工作目录下的模型Test.cae
        mdb = openMdb(pathName='Test.cae')
        o = mdb.models['myModel'].rootAssembly
        inst3 = o.instances['Part-2-1']
        myResult = getByFeature(inst3, length=10.0,radius=5.0,area=150)
        print myResult['EdgeFromLength']
        print len(myResult['EdgeFromRadius'])
        print len(myResult['FaceFromArea'])
    except Exception as e:
        print e
    