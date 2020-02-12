# -*- coding: utf-8 -*-
import sys, array, os
path = os.path.join(sys.path[0], 'Tensile.inp')
f = open(path)
c = f.readlines()
f.seek(0)
d = f.xreadlines()
f.seek(0)
e = f.readline()
f.close()
print "readlines: comsume %i byte"%sys.getsizeof(c)
print "xreadlines:comsume %i byte"%sys.getsizeof(d)
print "readline:  comsume %i byte"%sys.getsizeof(e)