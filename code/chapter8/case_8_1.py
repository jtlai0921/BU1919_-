# -*- coding: utf-8 -*-
import io

"""this is a example for chapter 7 file and dir"""

#�����ļ�hello.inp��д������
output=open("hello.inp",'w')
tempStrs=["hello", "", "CAEer"]
for str in tempStrs:
    str=str+'\n'
    output.writelines(str)
output.close()

#��ȡ�ļ�hello.inp����ӡ����Ļ��
input=open("hello.inp", 'r')
tempStrs=input.readlines()
print len(tempStrs)
for str in tempStrs:
    print str
input.close()
