# -*- coding: mbcs -*-
import os, os.path, sys
from odbAccess import *
elementL = 644
instanceL = 'PART-2-1'
times, stress = [], []
o = openOdb(path='myJob.odb', readOnly=False)
inst = o.rootAssembly.instances[instanceL]
ele = inst.getElementFromLabel(label=elementL)
frames = o.steps['myStep1'].frames
for frame in frames:
    times.append(frame.frameValue)
    fopS = frame.fieldOutputs['S']
    fopSFromEle = fopS.getSubset(region=ele)
    stress.append(fopSFromEle.values[0].mises)
o.close()
stressData = zip(times,stress)
plotData =  session.XYData(data=stressData,name='Stress at element 644',
    xValuesLabel='Time s',yValuesLabel='Stress Mpa')
stressCurve = session.Curve(xyData=plotData)
stressPlot = session.XYPlot(name='Stress Plot')
stressPlot.title.setValues(text='Stress at element 644')
chartName = stressPlot.charts.keys()[0]
chart = stressPlot.charts[chartName]
chart.setValues(curvesToPlot=(stressCurve,), )
chart.gridArea.style.setValues(color='White')
chart.legend.area.style.setValues(color='Gray')
myViewport = session.Viewport(name='myViewport',border=OFF,
    titleBar=OFF,titleStyle=CUSTOM)
myViewport.setValues(width=120,height=80,origin=(0,-20))
myViewport.setValues(displayedObject=stressPlot)
session.printToFile(fileName='stressPlot', format=PNG, canvasObjects=(
     myViewport, ))