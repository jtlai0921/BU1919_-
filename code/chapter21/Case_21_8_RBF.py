# -*- coding:utf-8 -*-
import pickle
import numpy as np
from scipy import interpolate as syip

#=====Fit the parameter of functoin from data.
output = open('data.pkl', 'rb')
x = pickle.load(output)
y = pickle.load(output)
z = pickle.load(output)
output.close()
x = np.array(x)
y = np.array(y)
z = np.array(z)
RBFFit = syip.Rbf(x,y,z,function='gaussian')
print RBFFit(4.0, 0.8), RBFFit(5.0, 0.8)
#=====Generate the data for further plot
x1 = np.linspace(2, 15, 15)
y1 = np.linspace(0.2, 1.5, 15)
x1 , y1 = np.meshgrid(x1,y1)
zfit = RBFFit(x1, y1)
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