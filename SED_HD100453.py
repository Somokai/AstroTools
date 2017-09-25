# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 18:40:56 2016

@author: somokai
"""


import matplotlib as mlt
#import matplotlib.pyplot as plt
import idlsave
import numpy as np
#from astropy.io import fits

mlt.use('Agg')

dir = ('C:/Users/Somokai/Dropbox/Research/Astropy/SED/')

a = idlsave.read(dir + 'hd100453_iras.sav')
b = idlsave.read(dir + 'hd100453_2MASS.sav')
c = idlsave.read(dir + 'hd100453_jhklm_fouque92.sav')
d = idlsave.read(dir + 'hd100453-mmM02.sav')
e = idlsave.read(dir + 'hd100453_irs.sav')
f = idlsave.read(dir + 'hd100453_iuelfl.sav')
g = idlsave.read(dir + 'hd100453_iras.sav')
h = idlsave.read(dir + 'hd100453_ubvjhklm_malfait_rev.sav')

'''plt.plot(a.w, a.lfl, 'ro', color='red')
plt.plot(b.w, b.lfl,'ro', color='green')
plt.plot(c.w, c.lfl,'ro', color='orange')
plt.plot(d.w, d.lfl,'ro', color='black')
plt.plot(e.wsl2r, e.lflsl2r)
plt.plot(e.wsl1r, e.lflsl1r)
plt.plot(e.w1, e.lfl1)
plt.plot(e.w2, e.lfl2)
#plt.plot(f.wl, f.lflls, 'ro')
plt.plot(f.ws, f.lfls)
plt.plot(g.w, g.lfl,'ro', color='purple')
plt.plot(h.w, h.lfl,'ro', color='cyan')

plt.title('SED')
plt.ylabel('$\lambda F_\lambda (W/m^2)$')
plt.xlabel('$\lambda (\mu m)$')
plt.yscale('log')
plt.xscale('log')

plt.savefig('SED.pdf')'''

xData = np.hstack([a.w, b.w, c.w, d.w, e.wsl2r, e.wsl1r, e.w1, e.w2, f.ws, g.w, h.w])
yData = np.hstack([a.lfl, b.lfl, c.lfl, d.lfl, e.lflsl2r, e.lflsl1r, e.lfl1, e.lfl2, f.lfls, g.lfl, h.lfl])

np.savetxt('data.csv', np.transpose([xData, yData]), delimiter=',')