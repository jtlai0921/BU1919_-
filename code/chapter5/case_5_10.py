# -*- coding: utf-8 -*-
for i in range(4):
    j = i
    while j<3:
        if j>=2:
            print 'Break here i = ' + str(i)
            break
        else:
            j = j + 1
    else:
        print 'No break occur!\nj = ' + str(j)
    print 'In for expr: i = ' + str(i)
print 'End of programm'