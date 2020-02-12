# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import os, re, random, os.path, sys
from scipy import optimize
from scipy import interpolate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
path = sys.path[0]
reportPath = os.path.join(path, 'CreepFittingReport.pdf')
figPath = os.path.join(path, 'fig.png')
#global parameter for matplotlib
colorList = ['k','b','r','c','m','y','g']
styleList = ['-','--',':','_']

#fitting func with 5 parameters: fixed temperature, fitting time and stress
def creepF(para, t, S, Tc):                   
    c1, c2, c3, c5, c6 = para
    t = np.array(t)
    S = np.array(S)
    Tc = np.array(Tc)
    return c1*np.power(S, c2)*np.power(t, (c3+1.0))/(c3 + 1.0) \
        + c5*np.power(S, c6)*t
    
def residF(para, strain, t, S, Tc):
    return strain - creepF(para, t, S, Tc)

# A class definiation for creep data processing
# create by tsu
# built at May 23 2013
# modified at May 28 2013
class creepProcessing:
    name = 'unnamed'    
    def __init__(self, dataPath=""):
        try:
            self.dataFile = open(dataPath)
        except IOError:
            print "Define the data by settingData"
            self.dataFile = None
        finally:
            self.t = []
            self.Tc = []
            self.S = []
            self.strain = []
            self.dataNum = 0
            self.dataList = []
    
    def settingData(self, t, Tc, S, strain, dataList, dataNum):
        self.t = np.array(t)
        self.Tc = np.array(Tc)
        self.S = np.array(S)
        self.strain = np.array(strain)
        self.dataList = np.array(dataList)
        self.dataNum = dataNum
    
    #Function designed to extract stress and temperature from string
    #"18.0Mpa60oC" ----> stress: 18.0Mpa & temperature: 60oC
    def splitStr(self, StressTemp):
        x1 = re.split('creep|Creep|Mpa|mpa|MPa|oC', StressTemp)
        n1 = re.search('Mpa|mpa|MPa', StressTemp).span()
        n2 = re.search('oC', StressTemp).span()
        if n1[0] < n2[0]:
            return [float(x1[0]), float(x1[1])]
        else:
            return [float(x1[1]), float(x1[0])]
    
    #Function designed to read and convert data from data file.
    def dataPre(self):
        stress = 0
        temper = 0
        if self.dataFile==None:
            return 0
        for item in self.dataFile.readlines():
            if not(re.match('from file|Generated by', item)):
                if not(len(item)-1):
                    self.dataList.append([[],[],[],[],[]])
                    self.dataNum += 1
                    pass
                elif re.search('Mpa|mpa|MPa', item) and re.search('oC', item):
                    stress,temper = self.splitStr(item)
                    pass
                else:
                    x1 = re.split(' +',item)
                    self.dataList[-1][0].append(float(x1[1]))
                    self.dataList[-1][1].append(stress)
                    self.dataList[-1][2].append(temper+273.15)
                    self.dataList[-1][3].append(float(x1[2])/100.0)
                    self.t.append(np.power(10,float(x1[1])))
                    self.Tc.append(temper+273.15)
                    self.S.append(stress)
        self.dataFile.close()            
        self.dataList = np.array(self.dataList)
        self.t = np.array(self.t)
        self.Tc = np.array(self.Tc)
        self.S = np.array(self.S)
        for esList in self.dataList:
            tempStrain = esList[3][0] + (esList[3][1] - esList[3][0])/(
                esList[0][1] - esList[0][0])*(-2.0 - esList[0][0])
            esList[4] = np.array(esList[3])-tempStrain
            self.strain = np.concatenate((self.strain, esList[4]), axis=0)
    
    #Function designed to fitting 5 parameter curve;
    #Flag "success" get values: 1,2,3,...,6,8; 
    # 1-4 means acceptable fitting
    def cfFun(self, iniPara, residFun):
        pp, success = optimize.leastsq(residFun, np.array(iniPara), 
                                        args=(self.strain, self.t, self.S, 
                                        self.Tc))
        return pp, success
    
    #Function designed to plot the 5 parameter curve fitting result
    def creepPlot(self, Para, creepF):
        tempTime = []
        tempStrain = []
        tempStrainC = []
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(1,1,1)
        for i in range(self.dataNum):
            colorNum = i%len(colorList)
            item = self.dataList[i]
            tempTime = np.power(10.0, item[0])
            tempStress = item[1]
            tempTemp = item[2]
            tempStrain = item[4]
            tempLabel = str(item[1][1])+" Mpa"
            tempTimeC = np.linspace(1, 10000, 10000)
            tempStressC = np.ones(10000)*item[1][0]
            tempTempC = np.ones(10000)*item[2][0]
            tempStrainC = creepF(Para,tempTimeC,tempStressC,tempTempC)
            ax.plot(tempTime, tempStrain, 'o', color=colorList[colorNum])
            ax.plot(tempTimeC, tempStrainC, color=colorList[colorNum], ls='-',
                lw=2, label=tempLabel)
        ax.legend(ncol=2, loc=2)
        ax.set_xscale('log')
        ax.text(2.0, self.strain.max()*0.45, r'$\varepsilon_{cr} = \frac{C_1 \sigma ^ {C_2} t ^ {C_3 + 1}}{C_3+1.0} + C_5 {\sigma ^ {C_6}} t$', fontsize=20)
        ax.axis([1.0,1.0e4, self.strain.min(), self.strain.max()])
        ax.set_ylabel("strain %")
        ax.set_xlabel("time h")
        fig.savefig(figPath)
    #Function designed to generate the curve fitting result
    def reportGenerate(self, iniPara0, residFun):
        self.dataPre()
        pp, success = self.cfFun(iniPara0, residF)
        self.creepPlot(pp, creepF) #generate the figure
        pp2out = ['%.3e'%i for i in pp]
        c = canvas.Canvas(reportPath, pagesize=A4)
        c.setFont('Times-BoldItalic',20)
        c.drawString(inch, 10.0 * inch, 
            "Summary of creep data fitting at %d oC" %(self.Tc[-1]-273.15))
        c.setFont('Times-Roman',10)
        c.drawCentredString(4.135 * inch, 0.75 * inch,
            'Page %d' % c.getPageNumber())
        c.drawImage(figPath, 0.0, inch*3)
        c.setFont('Times-Roman',16)
        c.drawString(inch*0.5, 2.5*inch, 'Fitting result: %s' % str(pp2out))
        c.drawString(inch*0.5, 2.0*inch, 'Fitting flag: %i' % success)
        c.setLineWidth(2)
        c.setStrokeColorRGB(0,0,0)
        c.showPage()
        c.save()
if __name__ == '__main__':
    # define the input and give the guess feed of the parameters
    dataPathcreep = os.path.join(path, '80_Noryl 731 Campus data.txt')
    iniPara0 = [0.0,3.0,-0.9,0.0,0.0]
    myCreepFitting = creepProcessing(dataPathcreep)
    myCreepFitting.reportGenerate(iniPara0, residF)