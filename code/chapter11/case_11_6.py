# -*- coding: utf-8 -*-
def test1():
    temp = [i**2 for i in range(100) if i%3==0]
    return temp
def test2():
    temp = []
    for i in range(100):
        if i%3==0:
            temp.append(i**2)
    return temp
if __name__=='__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    t2 = Timer("test2()", "from __main__ import test2")
    print "List comprehension consume:"+ str(t1.timeit(number=10000))+' s'
    print "Normal list-For loop consume:"+ str(t2.timeit(number=10000))+' s'