# -*- coding:utf-8 -*-
import pickle
import numpy as np
from scipy import optimize as syop

def f4fit(v, *args):
    x, y = v#x refer to the fit number and y refer to thickness.
    ab0, a1, b3 = args
    return ab0*x*y + a1*x + b3*y**3
#=====Fit the parameter of functoin from data.
output = open('data.pkl', 'rb')
x = pickle.load(output)
y = pickle.load(output)
z = pickle.load(output)
output.close()
x = np.array(x)
y = np.array(y)
z = np.array(z)
v = np.array([x,y])
guess = [1.0, 1.0, 1.0]
params, params_cov = syop.curve_fit(f4fit,v,z,guess)
resd = [z[i] - f4fit([x[i],y[i]], *params) for i in range(len(x))]
DV = np.sum((np.array(resd))**2)/len(x)
print params
print params_cov
print DV
#=====Generate the data for further plot
x1 = np.linspace(2, 15, 15)
y1 = np.linspace(0.2, 1.5, 15)
x1 , y1 = np.meshgrid(x1,y1)
v1 = np.vstack([x1.flatten(),y1.flatten()])
zfit = f4fit(v1, *params)
zfit = zfit.reshape((15,15))
#======Visualize the data
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(x, y, z, s=90, marker='o')
wf = ax.plot_wireframe(x1,y1,zfit, rstride=1, cstride=1)
ax.set_xlabel('Partical Numbers (-)')
ax.set_ylabel('Thickness of pen (mm)')
ax.set_zlabel('Max insert Force (N)')
plt.show()