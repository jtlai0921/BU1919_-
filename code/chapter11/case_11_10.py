# -*- coding: utf-8 -*-
import sys, array
a = [1,2,3,4,5]
b = (1,2,3,4,5)
c = {1:1,2:2,3:3,4:4,5:5}
x = array.array('l',a)
print "tuple: comsume %i byte"%sys.getsizeof(b)
print "list : comsume %i byte"%sys.getsizeof(a)
print "dict : comsume %i byte"%sys.getsizeof(c)
print "array: comsume %i byte"%sys.getsizeof(x)