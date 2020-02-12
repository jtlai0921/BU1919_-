# -*- coding: utf-8 -*-
i = 0
while (i<10):
    print 'Now i = ' + str(i)
    if i%3==2:
        print 'break occurs!'
        continue
    i=i+1
print 'End of programm'