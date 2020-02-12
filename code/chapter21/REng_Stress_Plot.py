# -*- coding: mbcs -*-
from math import *
from abaqus import *
from abaqusConstants import *
from caeModules import *

def deterP0(r1, d, Dd, E1=210000.0, E2=100000.0, mu=0.3):
    """calculate the hoop stress of sleeve during the interference fit"""
    if (Dd<0.0):
        return 0
    else:
        r2 = r1 + d
        K = 1.0/r1**2-1.0/r2**2
        K1 = (1.0 + mu)/K/r1/E2
        K2 = (1.0 - mu)*r1/K/r2**2/E2
        K3 = (1.0 - mu)*r1/E1
        P0 = Dd/(K1 + K2 + K3)
        A, C = -P0/K, P0/K/r2**2/2.0
        return 2.0*C-A/r1**2

vp = session.viewports['Viewport: 1']
r1_ = [25.0 + 0.1*i for i in range(1000)]#25.0#shaft a
Dd_ = 0.1#interference value
d_ = 2.0#[2.0 + 0.01*i for i in range(1000)]#thickness of the sleeve
S_ = [deterP0(item, d_, Dd_) for item in r1_]
Datas = zip(r1_, S_)
data = session.XYData(data=Datas,name='curveData', xValuesLabel='Thickness',
    yValuesLabel='Hoop stress')
sCurve = session.Curve(xyData=data)
sCurve.setValues(displayTypes=(SYMBOL,), useDefault=OFF)
sCurve.symbolStyle.setValues(marker=HOLLOW_CIRCLE,size=1.0,color='Black')
phPlot = session.XYPlot(name='Result')
#phPlot.title.setValues(text='Result of Shrink Fit')
chartName = phPlot.charts.keys()[0]
chart = phPlot.charts[chartName]
chart.setValues(curvesToPlot=(sCurve,), )
chart.gridArea.style.setValues(color='White')
#chart.legend.area.style.setValues(color='Gray')
vp.setValues(width=180,height=150,origin=(0,-120))
vp.setValues(displayedObject=phPlot)