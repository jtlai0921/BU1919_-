# -*- coding: utf-8 -*-
"""this is a example for chapter 8 file and dir"""
import csv
#创建文件hello.csv并写入内容
Wfile=file("hello.csv", "wb")
csvW=csv.writer(Wfile)
tempStrs=[['hello'], ['CAEer'], ['You', 'are', 'not', 'alone!']]
for str in tempStrs:
    csvW.writerow(str)
Wfile.close()

#读取文件hello.csv并打印在屏幕上
Rfile=file("hello.csv", "rb")
csvR=csv.reader(Rfile)
for str in csvR:
    for item in str:
        print item
Rfile.close()