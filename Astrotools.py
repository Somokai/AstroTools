# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:33:40 2016

@author: Somokai
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import cm
import matplotlib




def integ_inten(x,y,r,img):
    row = 0
    flux = 0
    temp = r
    while row < r:
        i = 0
        while i < 2*temp-1:
            flux = flux + img[(y-temp+i),(x+row)]
            if row > 0:
                flux = flux + img[(y-temp+i),(x-row)]
            i += 1
        row += 1
        temp -= 1
    return flux

def tilted_ring(img, th, center, a, b, intrad, norm, tilt):
    i=0
    flux_arrx = []
    flux_arry = []
    while i < 97:
        x1 = -a*np.cos(i*np.pi/48-130/180*np.pi)
        y1 = b*np.sin(i*np.pi/48-130/180*np.pi)
        y = (x1-center[1])*np.cos(th)-(y1-center[0])*np.sin(th)+center[1]
        x = (y1+center[0])*np.cos(th)+(x1-center[1])*np.sin(th)+center[0]
        flux = integ_inten(x,y,intrad,img)
        flux_arry.append(flux/norm)
        flux_arrx.append(i*180/48-tilt)
        i += 1
    #plt.plot(flux_arrx, flux_arry/max(flux_arry))
    plt.plot(flux_arrx, flux_arry, lw = 3)

def horizontal_ring(img, center, a, b, intrad, norm):
    flux_arrx = []
    flux_arry = []
    i = 0
    while i < 97:
        x1 = a*np.cos(i*np.pi/48+50/180*np.pi)
        y1 = b*np.sin(i*np.pi/48+50/180*np.pi)
        x = (x1+center2[0])  
        y = (y1+center2[1])
        flux = integ_inten(x,y,intrad,img)
        flux_arry.append(flux/norm)
        flux_arrx.append(i*180/48)
        i += 1
    plt.plot(flux_arrx, flux_arry/max(flux_arry), lw = 3)

def ring_oplot(img, center, a, b, intrad):
    flux_arrx = []
    flux_arry = []
    i = 0
    while i < 97:
        x1 = a*np.cos(i*np.pi/48)
        y1 = b*np.sin(i*np.pi/48)
        x = (x1+center[0])  
        y = (y1+center[1])
        pointx.append(x)
        pointy.append(y)
        flux = integ_inten(x,y,intrad,img)
        flux_arry.append(flux)
        flux_arrx.append(i*np.pi/48)
        i += 1

def circle_oplot(radius,center):
    pointy = []
    pointx = []
    i = 0
    while i < 97:
        x = radius*np.cos(i*np.pi/48)+center[1]
        y = radius*np.sin(i*np.pi/48)+center[0]
        pointx.append(x)
        pointy.append(y)
        i+=1
    points = [pointy, pointx]
    return (points)
        

def tilted_ring_oplot(img, th, center, a, b, intrad):
    i=0
    flux_arrx = []
    flux_arry = []
    while i < 97:
        x1 = a*np.cos(i*np.pi/48)
        y1 = b*np.sin(i*np.pi/48)
        x = (x1-center[0])*np.cos(th)-(y1-center[1])*np.sin(th)+center[0]
        y = (y1+center[1])*np.cos(th)+(x1-center[0])*np.sin(th)+center[1]
        pointx.append(x)
        pointy.append(y)
        flux = integ_inten(x,y,intrad,img)
        flux_arry.append(flux)
        flux_arrx.append(i*np.pi/48)
        i += 1            

def integ_rad(r1, r2, img, center,size):
    j = 0
    pixels = 0
    totAnn = 0
    x = []
    y = []
    while j < size:
        i = 0
        while i < size:
            r = np.sqrt(np.square(center[1]-j)+np.square(center[0]-i))
            #print(r)
            if r < r1 and r > r2:
                #print(r)
                #x.append(j)
                #y.append(i)
                pixels += 1
                totAnn += img[j][i]
                #print(totAnn)
            i += 1
        j += 1
    #plt.plot(x,y,'ro')
    plt.plot(center[0],center[1],'yo')
    print(totAnn)
    print(pixels)
    
    return [totAnn, pixels]
    
def back_subtract(backOutAnn, backInAnn, outObjAnn, inObjAnn, img, center,size):
    back = integ_rad(backOutAnn, backInAnn, img, center, size)
    intRadBack = back[0]
    pixelsB = back[1]
    background = intRadBack/pixelsB
    obj = integ_rad(outObjAnn, inObjAnn, img, center, size)
    intRadObj = obj[0]
    print(intRadObj)
    pixelsO = obj[1]
    subImg = intRadObj - background*pixelsO
    #background = intRadBack/(np.pi*(np.square(backOutAnn)-np.square(backInAnn)))
    #subImg = intRadObj - background*(np.pi*(np.square(outObjAnn)-np.square(inObjAnn)))
    circ1 = circle_oplot(backOutAnn, center)
    circ2 = circle_oplot(backInAnn, center)
    circ3 = circle_oplot(outObjAnn, center)
    circ4 = circle_oplot(inObjAnn, center)
    plt.imshow(img, origin = 'lower')
    plt.plot(circ1[0], circ1[1], 'r')
    plt.plot(circ2[0], circ2[1], 'r')
    plt.plot(circ3[0], circ3[1], 'y')
    plt.plot(circ4[0], circ4[1], 'y')
    plt.ylim([0, size])
    plt.xlim([0, size])
    print("Subtracted Flux")
    print(subImg)
    print("Background Flux/Pixel")
    print(background)

def find_center(center, image):
    i = -9
    j = -9
    sumx = 0
    sumy = 0
    sumi = 0
    while i < 10:
        while j < 10:
            sumx = sumx+(center[0]+i)*image[center[0]+i][center[1]+j]
            sumi = sumi+image[center[0]+i][center[1]+j]
            sumy = sumx+(center[1]+i)*image[center[0]+i][center[1]+j]
            j += 1
        i += 1
    x = sumx/sumi
    y = sumy/sumi
    return (x,y)


