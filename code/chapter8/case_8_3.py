# -*- coding: utf-8 -*-
"""this is a example for chapter 8 file and dir"""
import csv
#�����ļ�hello.csv��д������
Wfile=file("hello.csv", "wb")
csvW=csv.writer(Wfile)
tempStrs=[['hello'], ['CAEer'], ['You', 'are', 'not', 'alone!']]
for str in tempStrs:
    csvW.writerow(str)
Wfile.close()

#��ȡ�ļ�hello.csv����ӡ����Ļ��
Rfile=file("hello.csv", "rb")
csvR=csv.reader(Rfile)
for str in csvR:
    for item in str:
        print item
Rfile.close()