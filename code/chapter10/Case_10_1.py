# -*- coding:utf-8 -*-
import numpy as np
from scipy import interpolate as syip
x = np.linspace(0, 5, 10)
y = (x-2.5)**3
print x, y
result = syip.interp1d(x, y)
xx = np.linspace(0, 5, 100)
yy = result(xx)
import matplotlib.pyplot as plt
plt.plot(x, y, 'bo', label='Origin Data')
plt.plot(xx, yy, '-r', lw=2, label='linear interp')
plt.xlabel("x/xx")
plt.ylabel("y/yy")
plt.legend()
plt.show()