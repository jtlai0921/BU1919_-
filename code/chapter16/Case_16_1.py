# -*- coding: mbcs -*-
from odbAccess import *
from abaqusConstants import *
#==============Material read and write=======================
o = session.openOdb(name='HertzContact.odb', readOnly=False)
m = o.materials
m0 = m['STEEL']
print m0.name, m0.density.table, m0.elastic.table, m0.elastic.type
m1 = o.Material(name='NewSteel')
m1.Density(table=m0.density.table)
m1.Elastic(table=m0.elastic.table, type=m0.elastic.type)
o.save()
#==============Mesh information read=======================
o = session.openOdb(name='HertzContact.odb', readOnly=False)
p = o.parts
p1 = p['BASE']
print len(p1.nodes)

a = o.rootAssembly
i = a.instances
print i

ia = i['ASSEMBLY']
na = ia.nodes
print len(na)
na0_coord = na[0].coordinates
na0_label = na[0].label
na0_instance = na[0].instanceName

ib = i['BASE-1']
nb = ib.nodes
print len(nb)
eb = ib.elements
print len(eb)

nb0_coord = nb[0].coordinates
nb0_label = nb[0].label
nb0_instance = nb[0].instanceName