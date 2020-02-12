import math
from abaqusConstants import *
#=========================generate the data to plot=========================
xBase = range(0,50,1)
xData = [i*4.0*math.pi/50.0 for i in xBase]
y1Data = [math.sin(i) for i in xData]
y2Data = [math.cos(i) for i in xData]
sinData = zip(xData,y1Data)
cosData = zip(xData,y2Data)
sinData =  session.XYData(data=sinData,name='sinData',legendLabel='Sin(X)',
    xValuesLabel='X',yValuesLabel='Y')
cosData =  session.XYData(data=cosData,name='cosData',legendLabel='Cos(X)',
    xValuesLabel='X',yValuesLabel='Y')
#=========================generate the curve to plot========================
sinCurve = session.Curve(xyData=sinData)
sinCurve.setValues(displayTypes=(LINE,), legendLabel='sin(x) curve',
    useDefault=OFF)
sinCurve.lineStyle.setValues(style=SOLID,thickness=1.0,color='Black')
sinCurve.symbolStyle.setValues(show=OFF)
cosCurve = session.Curve(xyData=cosData)
cosCurve.setValues(displayTypes=(SYMBOL,), legendLabel='cos(x) curve',
    useDefault=OFF)
cosCurve.symbolStyle.setValues(marker=HOLLOW_CIRCLE,size=2.0,color='Black')
#============================generate picture===============================
scPlot = session.XYPlot(name='sin-cos-Plot')
scPlot.title.setValues(text='sin Vs. cos')
chartName = scPlot.charts.keys()[0]
chart = scPlot.charts[chartName]
chart.setValues(curvesToPlot=(sinCurve,cosCurve), )
chart.gridArea.style.setValues(color='White')
chart.legend.area.style.setValues(color='Gray')
myViewport = session.Viewport(name='myViewport',border=OFF,
    titleBar=OFF,titleStyle=CUSTOM,customTitleString=
    'Viewport Example of XYPlot')
myViewport.setValues(width=120,height=80,origin=(0,-20))
myViewport.setValues(displayedObject=scPlot)
session.printToFile(fileName='sin_cos', format=PNG, canvasObjects=(
     myViewport, ))