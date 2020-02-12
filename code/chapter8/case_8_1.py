# -*- coding: utf-8 -*-
import io

"""this is a example for chapter 7 file and dir"""

#创建文件hello.inp并写入内容
output=open("hello.inp",'w')
tempStrs=["hello", "", "CAEer"]
for str in tempStrs:
    str=str+'\n'
    output.writelines(str)
output.close()

#读取文件hello.inp并打印在屏幕上
input=open("hello.inp", 'r')
tempStrs=input.readlines()
print len(tempStrs)
for str in tempStrs:
    print str
input.close()
