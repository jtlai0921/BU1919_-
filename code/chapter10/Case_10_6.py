# -*- coding:utf-8 -*-
import sys, os.path
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
path = sys.path[0]
localPath = os.path.join(path, 'hello.pdf')
c = canvas.Canvas(localPath, pagesize=A4)
c.translate(inch,inch)
tOb = c.beginText()
tOb.setTextOrigin(inch*0.5, inch*3.5)
tOb.setFont("Times-Roman", 15)
tOb.textLines("""
This is a picture for the stress at P1 and P2 along with the loading process.
""")
c.drawText(tOb)
data1 = [0.0,5.0,9.0,2.0,10.0,15.0]
data2 = [2.0,3.0,6.0,9.0,10.0,16.0]
t = [1,2,3,4,5,6]
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(1,1,1)
ax.plot(t, data1, 'bo', lw=2, label="S11@P1")
ax.plot(t, data2, '-r', lw=2, label="S11@P2")
ax.legend()
ax.set_ylabel("Stress (Mpa)")
ax.set_xlabel("Time (s)")
cFig = fig.savefig('xxx.tif')
c.drawImage('xxx.tif', 0.0, inch*4)
c.showPage()
c.save()