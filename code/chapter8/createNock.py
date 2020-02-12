# -*- coding: utf-8 -*-

"""this is a example for chapter 7 file and dir"""

from sys import *
from math import *
from re import *

#这个例子我们利用Tensile.inp文件来生成一个带缺口的拉伸试验模拟的INP文件
inpName='Tensile'
inpName1=inpName+'.inp'
f1=open(inpName1,'r')
newName='Nock_'+inpName1
f2=open(newName,'w')
s1=f1.readlines()
meshSize=0.0015
for s in s1:
	cord_s=s
	cord_modify=sub(',',' ',cord_s)
	cord_modify=split(' +',cord_modify)
	if len(cord_modify)==4:
		nodeLable=cord_modify[1]
		if nodeLable=='1373':
			cord_mod_x=float(cord_modify[2])-0.4*meshSize
			f2.write('   1373,  '+str(cord_mod_x)+',  '+cord_modify[3])
		elif nodeLable=='1374':
			cord_mod_x=float(cord_modify[2])-0.8*meshSize
			f2.write('   1374,  '+str(cord_mod_x)+',  '+cord_modify[3])
		elif nodeLable=='1375':
			cord_mod_x=float(cord_modify[2])-1.2*meshSize
			f2.write('   1375,  '+str(cord_mod_x)+',  '+cord_modify[3])
		elif nodeLable=='1376':
			cord_mod_x=float(cord_modify[2])-1.6*meshSize
			f2.write('   1376,  '+str(cord_mod_x)+',  '+cord_modify[3])
		elif nodeLable=='1377':
			cord_mod_x=float(cord_modify[2])-2.0*meshSize
			f2.write('   1377,  '+str(cord_mod_x)+',  '+cord_modify[3])
		else:
			f2.write(s)
	else:
			f2.write(s)
f1.close()
f2.close()
#os.remove(new1_testINP)