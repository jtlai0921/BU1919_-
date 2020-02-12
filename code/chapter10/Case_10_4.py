# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
#===================define the function======================
def rangeCal(FAT,*cycles):
    rangeC=FAT*1.0
    rangeD=rangeC*(2.0/5.0)**(1.0/3.0)
    rangeL=rangeD*(5.0/100.0)**(1.0/5.0)
    range =[]
    temp1 =(2.0e6)**(1.0/3.0)*rangeC
    temp2 =(5.0e6)**(1.0/5.0)*rangeD
    for N in cycles:
        if N<=5e6:
            range.append(temp1/(N**(1.0/3.0)))
        elif N<=1e8:
            range.append(temp2/(N**(1.0/5.0)))
        else:
            range.append(rangeL)
    print "Detail category: "+str(rangeC)
    print "Constant amplitude fatigue limit: "+str(rangeD)
    print "Cut-off limit: "+str(rangeL)
    return {"PointsFAT":[rangeC,rangeD,rangeL],"Data":range}
#===================calculate the data=======================
FatNum1 = 90.0 #define Fatigue category of the situation
nCycle1 = [10**(i+j/10.0) for i in range(5,10) for j in range(1,10)]
Data1   = rangeCal(FatNum1, *nCycle1)
sRange1 = Data1["Data"] #calculate the S-N curve data
CSrange1= 90.0 #define the current stress range obtained from FEA
#=======================Plot the data========================
FATLabel1='FAT'+str(int(FatNum1))
plt.plot(nCycle1, sRange1, c='k', lw=2, label=FATLabel1)
CSLabel= "stressRange="+str(int(CSrange1))+ "Mpa"
plt.axhline(y=CSrange1, lw=2, c='r', ls='--', label=CSLabel)
plt.scatter(2e6, 90, s=50, c='b',marker='s')
plt.annotate('result: (2e6, 90)', (2e6, 90),  xycoords='data',
    xytext=(2e7, 130), textcoords='data',
    arrowprops=dict(arrowstyle="->",
    connectionstyle="angle3,angleA=0,angleB=-90"),)
plt.ylabel("Stress range in Mpa --->")
plt.xlabel("Number of cycles  --->")
plt.title('Fatigue evaluation according to IIW standard')
plt.xscale('log')
plt.legend()
plt.grid(True, which='both')
plt.show()