# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 22:29:44 2016

@author: Somokai
"""
import matplotlib.pyplot as plt

#ratio1 = [0.0458, 0.0438, 0.066]
#ratio2 = [0.0487, 0.0514, 0.091]
ratio1 = [0.0176, 0.021, 0.025]
wavelength = [1.02, 1.22, 1.63]
yerr = [0.0009, 0.001, 0.0009]
plt.plot(wavelength,ratio1, '-o' )#,label = 'Without thermal')
#plt.plot(wavelength,ratio2, '-o', label = 'With Thermal')
plt.errorbar(wavelength, ratio1,0, yerr)
plt.legend(loc = 2)
plt.semilogy()
plt.xlabel('Wavelength (um)')
plt.ylabel('fdisk/fstar')
plt.show()

