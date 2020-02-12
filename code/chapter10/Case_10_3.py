# -*- coding:utf-8 -*-
import numpy as np
from scipy import optimize as syop

def f(v):
    x, y = v
    return (1.0-x)**2 + 100.0*(y-x**2)**2
def fprime(v):
    x, y = v
    dx = 2.0*(x-1.0)-400.0*x*(y-x**2)
    dy = 200.0*(y-x**2)
    return np.array((dx,dy))
#=====find the min point of the function.
guess = [0.0, 0.0]
result = syop.fmin_bfgs(f, guess)
print result