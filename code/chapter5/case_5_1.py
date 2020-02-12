# -*- coding: utf-8 -*-
import os.path
path = 'D:\workspace_abaqus\wearTest.inp'
print 'Is \''+path +'\''+ ' a file?'
flag = os.path.isfile(path)
print flag
s = path.split('.')
print 'The type of the file is ' + s[1]