# -*- coding: utf-8 -*-
dict0 = {'first':1, 'second':2, 'red':2}
for (key, value) in dict0.iteritems():
    print '%-8s'%key+' = '+'%4s'%str(value)
print '-'*30
for key in dict0.iterkeys():
    print '%-8s'%key+' = '+'%4s'%str(dict0[key])
print '-'*30
for value in dict0.itervalues():
    print '%-8s'%'????'+' = '+'%4s'%str(value)
print '-'*30
print 'End of programm'