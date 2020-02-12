# -*- coding: mbcs -*-
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
###################parameters#################################
R = 3.0
Press = 10.0
#Mdb()
vp = session.viewports['Viewport: 1']
#=========================generate the theory data to plot==================
angles = [pi/2.0/16.0*i for i in range(0,17,1)]
xData = [R*a for a in angles]
yData = [Press/2.0*(2.0-4.0*cos(2.0*a)) for a in angles]
theoData = zip(xData,yData)
xQuantity = visualization.QuantityType(type=PATH)
yQuantity = visualization.QuantityType(type=STRESS)
theoData = session.XYData(data=theoData,name='Theory',legendLabel='Theory',
    axis1QuantityType=xQuantity, axis2QuantityType=yQuantity)
theoCurve = session.Curve(xyData=theoData)
theoCurve.setValues(displayTypes=(LINE,), legendLabel='Theory', 
    useDefault=OFF)
theoCurve.lineStyle.setValues(style=SOLID,thickness=2.0, color='Black')
#============================generate picture===============================
phPlot = session.XYPlot(name='Stress distributte')
phPlot.title.setValues(text='Stress around the hole')
chartName = phPlot.charts.keys()[0]
chart = phPlot.charts[chartName]
chart.setValues(curvesToPlot=(theoCurve,), )
chart.gridArea.style.setValues(color='White')
chart.legend.area.style.setValues(color='Gray')
phPlot.title.style.setValues(
    font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
chart.legend.textStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-180-*-*-p-*-*-*')
chart.legend.titleStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-180-*-*-p-*-*-*')
chart.axes1[0].labelStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
chart.axes1[0].titleStyle.setValues(
    font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
chart.axes2[0].labelStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
chart.axes2[0].titleStyle.setValues(
    font='-*-arial-medium-r-normal-*-*-200-*-*-p-*-*-*')
vp.setValues(width=180,height=150,origin=(0,-20))
vp.setValues(displayedObject=phPlot)
session.printOptions.setValues(rendition=GREYSCALE, vpDecorations=OFF, 
    reduceColors=False)
session.printToFile(fileName='TheoryResult', format=PNG, canvasObjects=( vp, ))