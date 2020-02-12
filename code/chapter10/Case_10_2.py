# -*- coding:utf-8 -*-
import numpy as np
from scipy import optimize as syop

def f(v):
    x, y = v
    return (2.0*x**2 + 3.0*y**2)*(1.0+(np.random.random()-0.5)*0.2)
def f4fit(v, a, b):
    x, y = v
    return a*x**2 + b*y**2
#=====Fit the parameter of functoin from data.
N = 20
limit = 20
x = np.linspace(-1*limit, limit, N)
y = np.linspace(-1*limit, limit, N)
x , y = np.meshgrid(x,y)
v = np.vstack([x.flatten(),y.flatten()])
z = f(v)
guess = [1.0, 1.0]
params, params_con = syop.curve_fit(f4fit,v,z,guess)
print params
#=====Generate the data for further plot
x1 = np.linspace(-1*limit, limit, N*2)
y1 = np.linspace(-1*limit, limit, N*2)
x1 , y1 = np.meshgrid(x1,y1)
v1 = np.vstack([x1.flatten(),y1.flatten()])
zfit = f4fit(v1, *params)
zfit = zfit.reshape((N*2,N*2))
#======Visualize the data
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(x, y, z, c='y', marker='^')
surf = ax.plot_surface(x1,y1,zfit, rstride=1, cstride=1, cmap=cm.cool,
        linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()