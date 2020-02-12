# -*- coding: utf-8 -*-
def myfun0(i):
    ilist = [i**2 for i in range(i) if i%3 ==1]
    return ilist
def myfun1(i, j):
    ilist = [i**2 for i in range(i) if i%3 ==1]
    jlist = [i**2 for i in range(i) if i%3 ==0]
    return ilist,jlist
a0 = myfun0(9)
print 'a0 ='+str(a0)
a1 = myfun1(9, 9)
print 'a1 ='+str(a1)
print 'End of programm'