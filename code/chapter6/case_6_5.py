# -*- coding: utf-8 -*-
def fun1 (a, b):
    print a, b
def fun2 (a, b, c=2):
    print a, b, c
def fun3 (*a):
    if len(a)==0:
        print 'No data'
    else:
        print a
def fun4 (**a):
    if len(a)==0:
        print 'No data'
    else:
        print a
fun1(2,3)
fun1(a=2,b=3)
fun2(2,3)
fun2(a=2,b=3,c=4)
fun3(2,3,4)
fun4(a=2,b=3,c=4)
fun2(2,3,c=4)
print 'End of programm'