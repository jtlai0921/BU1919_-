# -*- coding: utf-8 -*-
ss = 'Hello!'
def myfun0():
    global ss
    print ss+' from fun0'
def myfun1(a):
    global ss
    ss = a
def myfun2(a, b):
    pass
myfun0()
myfun1('Welcome!')
myfun0()
myfun2(1,2)
print 'End of programm'