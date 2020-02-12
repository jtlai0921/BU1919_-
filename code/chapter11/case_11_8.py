# -*- coding: utf-8 -*-
import numpy as np
row = 100
col = 100
def test1():
    x = [[1 for j in xrange(col)] for i in xrange(row)]
    return x
def test2():
    x = np.ones((row,col), np.int)
    return x
if __name__=='__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    t2 = Timer("test2()", "from __main__ import test2")
    print "Home-code consume:"+ str(t1.timeit(number=1000))+' s'
    print "Numpy     consume:"+ str(t2.timeit(number=1000))+' s'