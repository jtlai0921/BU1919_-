# solver.py
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
############################
def fun2Solve(para, *arg):
    a, x0, y0 = para[0], para[1], para[2]
    p1, p2, Lth = arg[0][0], arg[0][1], arg[0][2]
    return [length(p1[0], p2[0], para) - Lth,
        catenary(p1[0], para) - p1[1],
        catenary(p2[0], para) - p2[1]]
#Length of catenary
def length(x1, x2, arg):
    a, x0, y0 = arg[0], arg[1], arg[2]
    return a*(sh_f(np.abs(x1-x0)/a)+sh_f(np.abs(x2-x0)/a))
#Points on the coord of catenary
def catenary(x, arg):
    a, x0, y0 = arg[0], arg[1], arg[2]
    return a*(ch_f((x-x0)/a)-1.0) + y0
#Math func: sh
def sh_f(x):
    return (np.exp(x)-np.exp(-1.0*x))/2.0
#Math func: ch
def ch_f(x):
    return (np.exp(x)+np.exp(-1.0*x))/2.0
if __name__=='__main__':
    guess = [10.0, 0.0, 0.0]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    mL = ['o', 'v', '1', 's', 'p', '+']
    for i in range(6):
        inputs = [(0.0, 0.0), (500.0-60.0*i, -80.0*i), 1000.0]
        p = optimize.fsolve(fun2Solve, guess, inputs)
        x = np.arange(0.0, 500.0-60.0*i, 8)
        y = catenary(x, p)
        ax.plot(x, y, c='black', marker=mL[i], ms=5.0, 
            label="Catenary"+str(i))
    ax.legend(ncol=2, loc=4)
    ax.set_xlim(0, 500)
    ax.set_ylim(-800, 0)
    ax.set_ylabel("Y")
    ax.set_xlabel("X")
    plt.show()
    #cFig = fig.savefig('xxx.png')