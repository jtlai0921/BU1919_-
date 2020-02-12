# -*- coding: utf-8 -*-
def test1():
    "function join"
    tempS = ['str']*1000
    return ''.join(tempS)
def test2():
    "operate +"
    tempS = ['str']*1000
    tempS0=''
    for i in tempS:
        tempS0 = tempS0 + i
    return tempS0
if __name__=='__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    t2 = Timer("test2()", "from __main__ import test2")
    print "function join consume:"+ str(t1.timeit(number=10000))+' s'
    print "operate + consume:"+ str(t2.timeit(number=10000))+' s'