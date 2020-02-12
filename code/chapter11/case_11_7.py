# -*- coding: utf-8 -*-
import os
dir_ = os.getcwd()
path_ = os.path.join(dir_, 'Tensile.inp')
def test1():
    f = open(path_)
    x = ''
    for line in f.readlines():
        x = line
        if not x:
            break
    f.close()
def test2():
    f = open(path_)
    x = ''
    while 1:
        x = f.readline()
        if not x:
            break
    f.close()
if __name__=='__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    t2 = Timer("test2()", "from __main__ import test2")
    print "Readlines consume:"+ str(t1.timeit(number=100))+' s'
    print "Readline  consume:"+ str(t2.timeit(number=100))+' s'