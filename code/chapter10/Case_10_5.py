# -*- coding:utf-8 -*-
import sys, os.path
from xlwt import Workbook
path = sys.path[0]
w = Workbook()
ws = w.add_sheet('test')
for i in xrange(10):
    ws.write(i,2,i)
localPath = os.path.join(path, 'example.xls')
w.save(localPath)