# -*- coding: utf-8 -*-
def fun0 (a, b=1, *c, **d):
    print a, b, c, d
fun0(2,3)
fun0(2,3,4)
fun0(2,3,4,5)
fun0(a=2,b=3,c=4)
print 'End of programm'