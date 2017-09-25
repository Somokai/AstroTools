# -*- coding: utf-8 -*-
"""
Created on Thu May 19 20:18:01 2016

@author: Somokai
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np


def integ_inten(x,y,r,img):
    row = 0
    flux = 0
    temp = r
    while row < r:
        i = 0
        #print(temp)
        while i < 2*temp+1:
            flux = flux + img[(x-temp+i),(y+row)]
            #print(i)            
            if row > 0:
                flux = flux + img[(x-temp+i),(y-row)]
            i += 1
        row += 1
        temp -= 1
        #print(row)
    return flux
            

hdus = fits.open('C:/Users/Somokai/Dropbox/Research/HD100453/Plots/Fits Images/HIP56354_ifs_science_median_H.fits')
img1 = hdus[0].data

hdus = fits.open('C:/Users/Somokai/Dropbox/Research/HD100453/Plots/Fits Images/e_IH_5.0_-30.0_I_img_psfconvolved.fits')
img2 = hdus[0].data


#plt.imshow(img1, origin = 'lower')

#plt.imshow(img2, origin = 'lower')

points_east = [[164, 160], [156, 166], [148, 168], [140, 167], [132, 168], [124, 163], [116, 154]]
points_west = [[170, 112], [162, 121], [154, 121], [146, 121], [138, 120], [130, 124], [122, 131]]


points_Meast = [[193, 182], [183, 146], [167, 210], [154, 220], [131, 228], [111, 225], [92, 221]]
points_Mwest = [[126, 89], [137, 78], [149, 72], [172, 67], [194, 72], [208, 78], [226, 88]]

n = len(points_east)

#print(img)

flux_east = []
flux_west = []

flux_Meast = []
flux_Mwest = []

i = 0

while i < n:
    fluxe = integ_inten(points_east[i][0], points_east[i][1], 3, img1)
    fluxw = integ_inten(points_west[i][0], points_west[i][1], 3, img1)
    flux_east.append(fluxe)
    flux_west.append(fluxw)
    i += 1

i = 0

fluxep = 0

while i < n:
    fluxe = integ_inten(points_Meast[i][0], points_Meast[i][1], 3, img2)
    fluxw = integ_inten(points_Mwest[i][0], points_Mwest[i][1], 3, img2)
    flux_Meast.append(fluxe)
    flux_Mwest.append(fluxw)
    i += 1

i = 0

flux_east = flux_east/max(flux_east)
flux_Meast = flux_Meast/max(flux_Meast)

flux_west = flux_west/max(flux_west)
flux_Mwest = flux_Mwest/max(flux_Mwest)
 
print(flux_east)
#flux_west = flux_west/max(flux_west)

#plt.plot(flux_Meast)
#plt.plot(flux_east)

plt.plot(flux_Mwest)
plt.plot(flux_west)
#print('South = ' + str(flux_east))
#print('North = ' + str(flux_west))