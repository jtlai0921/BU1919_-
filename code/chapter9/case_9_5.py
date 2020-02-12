# -*- coding: utf-8 -*-
"""this is a example for chapter 9 """
from case_9_4 import FEMError as FEEr

class FE_Model(object):
    def __init__ (self, node=None, element=None, BC=None):
        self.node = node
        self.element = element
        self.BC = BC
    def checkNode (self):
        if self.node==None:
            raise FEEr, ('myFEM', 'Miss nodes file')
        else:
            return 1
    def checkElement (self):
        if self.element==None:
            raise FEEr, ('myFEM', 'Miss elements file')
        else:
            return 1
    def checkBC (self):
        if self.BC==None:
            raise FEEr
        else:
            return 1
    def solve (self):
        pass
if __name__=='__main__':
    f1 = FE_Model(element='eles.inp')
    try:
        f1.checkNode()
    except FEEr, e:
        print 'FEMError found! ', e
    try:
        f1.checkBC()
    except FEEr, e:
        print 'FEMError found! ', e
    finally:
        print 'End of programm!'