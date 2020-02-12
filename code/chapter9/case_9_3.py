# -*- coding: utf-8 -*-
"""this is a example for chapter 9 """
try:
    f = open(r'C:\Python26\3x.py')
    a = 1/0
except StandardError, e:
    print 'StandardError: ', e
except IOError, e1:
    print 'IOError: Fail to open the file. ', e1
except ZeroDivisionError, e2:
    print 'ZeroDivisionError: Fail to do math operation. ', e2
else:
    print 'This is else block'