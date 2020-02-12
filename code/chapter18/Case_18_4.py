# -*- coding: mbcs -*-
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from Solver import fun2Solve
from Solver import catenary
############################
length = 10000.0#mm
pointA = (0.0, 0.0)#Final position of PointA
pointB = (5000.0, -1000.0)#Final position of PointB
############################
guess = [10.0, 2500.0, -1000]
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
mL = ['*', '|', 's', 'p', 'v']
sL = ['-', '-.', ':', '.']
inputs = [pointA, pointB, length]
pE = optimize.fsolve(fun2Solve, guess, inputs)
xs = np.arange(0.0, 5000.0, 8.0)
ys = catenary(xs, pE)
ax.plot(xs, ys, c='black',ls='-', lw=2.0, label=r'$Theory: stiff = \infty$')
data_file = open('data.pkl', 'rb')
for i in range(3):
    data = pickle.load(data_file)
    ax.plot(data[0], data[1], c='black', marker=mL[i], ms=6.0, 
        label=data[2])
data_file.close()
ax.legend(ncol=2, loc=4)
ax.set_xlim(0, 5000)
ax.set_ylim(-7000, 0)
ax.set_ylabel("Y")
ax.set_xlabel("X")
plt.show()