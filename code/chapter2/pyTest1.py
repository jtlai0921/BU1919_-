# -*- coding: utf-8 -*-

def is_prime(num):
    # Initial to presume it's a prime
    rt = True
    # To test the numbers if it can be divided exactly by a smaller number.
    for i in range(2, num):
        if num % i == 0:
            rt = False
            break
    return rt

a = []
b = {}
for i in range(1,10):
    if not(is_prime(i)):
        a.append(i)
    else:
        b["CompositeNumber"+str(i)*2] = i
for key,value in b.iteritems():
    print "%s = %s" % (key, value)
print "the prime numbers is %s" % a
