# -*- coding: utf-8 -*-
def test1():
    temp = 0
    for i in range(500):
        temp = (lambda x,y:x+y)(temp, i)
    return temp
def test2():
    temp = 0
    outLoop = lambda x,y:x+y
    for i in range(500):
        temp = outLoop(temp, i)
    return temp
if __name__=='__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    t2 = Timer("test2()", "from __main__ import test2")
    print "Function in Loop consume:"+ str(t1.timeit(number=10000))+' s'
    print "Function out Loop consume:"+ str(t2.timeit(number=10000))+' s'