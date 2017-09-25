# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:37:03 2017

@author: Somokai
"""


import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.io.idl import readsav
import gzip
import numpy as np
import os


#dir = ('/Users/Zac/Dropbox/Research/PDS70/Output/')
#dir = ('C:/Users/Somokai/Dropbox/Research/PDS70/Output/')
#dir = ('/Users/rachelfernandes/Dropbox/Research/PDS70/Output')
rstar = 1.25
tstar = 4400es
lumscale = 1
dis = 140

def plotter(count): 
    plt.clf()
	
    lines = np.loadtxt('peel_flux_45.0_0.0.dat', skiprows = 2)
	
    flux = []
    wavelength = []

    i = 0
    while i < len(lines):
        #print(lineP[i][0])
        wavelength.append(lines[i][0])
        flux.append(lines[i][1])
        i += 1
	
    sigma = 5.67e-5
    pc = 3.0857e18
    lsun = 3.845e33
    fnorm = lumscale/(4*3.1416)/dis**2/pc**2*lsun/1e3

    normFlux = []
    for n in flux:
        normFlux.append(n*fnorm)
        
    from astropy.io.votable import parse
    votable = parse("../SED/vizier_votable.vot")

    data_processed = {}
    clrcnt = 0
    prevstored = []
    clr = []


    table = votable.get_first_table()
    data = table.array
    for d in data:
        stored = str(d[7])
        stored = stored.strip("b'")
        stored = stored.split(":", 1)[0]
        #print(stored)
        if stored not in prevstored:
            clr.append(stored)
            clrcnt += 1
            prevstored.append(stored)
        #print(stored)
        #print(clrcnt)
        if stored in data_processed.keys():
            data_processed[stored].append([3E5/d[4],(d[5]*3E-12)/(3E5/d[4]),(d[6]*3E-12)/(3E5/d[4])])
        else:
            data_processed[stored] = []
            data_processed[stored].append([3E5/d[4],(d[5]*3E-12)/(3E5/d[4]),(d[6]*3E-12)/(3E5/d[4])])

    #print(data_processed)

    #print(data_processed)

    #print(xData)

    #fig, ax = plt.subplots()
    #ax.set_color_cycle(['blue','green','red','magenta','cyan', 'black', 'purple'])


    data = np.loadtxt('../Plots/lte44-4.5-0.0.spec.ascii')
    lumstar = 4*3.1416*(rstar*6.955e10)**2*sigma*tstar**4
    rstar2 = lumstar/(4*3.1416*sigma)/tstar**4
    atnorm = rstar2/dis**2/pc**2

    xData = []
    yData = []
    for d in data:
        xData.append(d[0])
        yData.append(d[1]/d[0]*2.9929e14*atnorm/1000)

    plt.plot(xData, yData)

    keys = []
    for key in data_processed.keys():
        keys.append(key)

    i = 0
    for value in data_processed.values():
        xData = []
        yData = []
        yError = []
        for d in value:
            #print(d)
            xData.append(d[0])
            yData.append(d[1])
            yError.append(d[2])
        #plt.plot(xData, yData, 'o', label = keys[i])
        plt.errorbar(xData, yData, yerr = yError, fmt = 'o', label = keys[i])
        i += 1

    a = readsav('../SED/psd70_irs.sav')

    plt.plot(a.W_LL1, a.LFL_LL1,'r-', color = 'red', label = "Spitzer")
    plt.plot(a.W_LL2, a.LFL_LL2,'r-', color = 'red')
    plt.plot(a.W_SL1, a.LFL_SL1,'r-', color = 'red')
    plt.plot(a.W_SL2, a.LFL_SL2,'r-', color = 'red')


    plt.plot(wavelength, normFlux,'black' )
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('$\lambda F_\lambda (W/m^2)$')
    plt.xlabel('$\lambda (\mu m)$')
    plt.legend(prop={'size':6})
    plt.xlim(0.08,4500)
    plt.ylim(10E-18,10E-13)
    plt.savefig('../Plots/SEDs/SED' + str(count) + '.png', dpi = 300)
    
    os.chdir(dir)
    print(dir)
    print('finished')
    

i = 0
while i < 30:
    plotter(i)
    i += 1

#f = open('data.txt', 'w')

#f.write(str(data_processed))'''