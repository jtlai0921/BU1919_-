# -*- coding: mbcs -*-
def getByRadius (source, radius, tol=1e-3):
    result={'Edge':[], 'coordY':[], 'coordX':[]}
    vets = source.vertices
    for e in source.edges:
        try:
            if abs(e.getRadius()-radius)<tol and abs(e.pointOn[0][2])<tol:
                vList = e.getVertices()
                result['Edge'].append(e)
                for idi in vList:
                    data = vets[idi].pointOn[0]
                    result['coordY'].append(data[1])
                    result['coordX'].append(data[0])
        except Exception as e:
            print e
    return result