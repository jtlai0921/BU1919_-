# -*- coding: utf-8 -*-
"""this is a example for chapter 8 file and dir"""
from sys import *
from re import *

inpName='Tensile'
inpName1=inpName+'.inp'
f1=open(inpName1,'r')
newName='Map_'+inpName1
f2=open(newName,'w')
s1=f1.readlines()
for s in s1:
	f2.write(s)
	ss=s.split()
	if len(ss)>=2:
		if (ss[0]=='*End')&(ss[1]=='Assembly'):
			translate_Y=12.0
			translate_vector='0.0,'+str(translate_Y)+',0.0'+'\n'
			f2.write('*Map solution\n')
			f2.write(translate_vector)
f1.close()
f2.close()
#os.remove(inpName1)