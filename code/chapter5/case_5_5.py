# -*- coding: utf-8 -*-
ab = [1, 2, 3.0, 'listEnd']
ABindex = range(len(ab))
for i in ABindex:
    print 'The '+str(i)+' element is '+str(type(ab[i]))+':'+str(ab[i])
print 'End of programm'