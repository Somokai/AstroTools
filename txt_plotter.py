# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 13:07:05 2016

@author: Somokai
"""

import pylab
import matplotlib.pyplot as plt

data = pylab.loadtxt('C:/Users/Somokai/Dropbox/Research/Astropy/Averaged_Photosphere.txt')

plt.plot( data[:,0], data[:,1])
plt.plot( data[:,0], data[:,2])

plt.loglog()

plt.legend()
plt.ylabel("Normalized Flux")
plt.xlabel("Wavelength")