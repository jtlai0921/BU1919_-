# -*- coding: utf-8 -*-
square = lambda x: x*x
sum = lambda x, y, z: x+y+z
xx = yy = zz = range(1,5)
print map(square, xx)
print map(sum, xx, yy, zz)
print 'End of programm'