# -*- coding: utf-8 -*-
def test1():
    "built-in function"
    aList = range(100)
    return sum(aList)
def test2():
    "home-code function1"
    aList = range(100)
    return reduce(lambda x,y:x+y, aList)
def test3():
    "home-code function2"
    temp = 0
    for i in range(100):
        temp = temp +i
    return temp
if __name__=='__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    t2 = Timer("test2()", "from __main__ import test2")
    t3 = Timer("test3()", "from __main__ import test3")
    print "built-in function consume:"+ str(t1.timeit(number=10000))+' s'
    print "home code function1 consume:"+ str(t2.timeit(number=10000))+' s'
    print "home code function2 consume:"+ str(t3.timeit(number=10000))+' s'