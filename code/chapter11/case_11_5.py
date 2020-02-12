# -*- coding: utf-8 -*-
def myADD (a, b):
    return a + b
def test1():
    temp = 0
    for i in range(500):
        temp = temp + i
    return temp
def test2():
    temp = 0
    for i in range(500):
        temp = myADD(temp, i)
    return temp
if __name__=='__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    t2 = Timer("test2()", "from __main__ import test2")
    print "No Funcall consume:"+ str(t1.timeit(number=10000))+' s'
    print "Call fromF consume:"+ str(t2.timeit(number=10000))+' s'