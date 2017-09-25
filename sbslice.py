# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:12:09 2016

@author: Somokai
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv

usr = 'Somokai'

#dir = 'C:/Users/'+ usr +'/Dropbox/Research/PDS70/Plots/'
dir = '../PDS70-ALMA-final2/'

def img_scale(text, loc, width):
    ax.text(loc[0]-14, loc[1]+5, text, color = 'white')
    ax.plot((loc[0], loc[0]+width),(loc[1],loc[1]), color = 'white', lw = 2)
    

def integ_inten(x,y,r,img):
    row = 0
    flux = 0
    temp = r
    count = 0
    while row < r:
        i = 0
        count += 1
        while i < 2*temp-1:
            flux = flux + img[(y-temp+i),(x+row)]
            #print((y-temp+i),(x+row),flux)
            #if row > 0:
            #    flux = flux + img[(y-temp+i),(x-row)]
            i += 1
            count += 1
        row += 1
        temp -= 1
    #print(count)
    return flux
            
def v_slice(slice, img, norm):
    i = 0
    flux = 0
    size = len(img[0])
    print(size)
    flux_arr = []
    while i < size:
        #flux = integ_inten(slice-1, i, intrad, img)
        flux_arr.append(img[i][slice-1]/norm)
        i += 1
    plt.plot(flux_arr)
    return(flux_arr)
    
def h_slice(slice, img, norm):
    plt.plot(img[slice-1]/norm)
    return(img[slice-1]/norm)
    
def d_slice(angle, img, norm, offset,centering,scale,intrad, normalize):
    flux = 0
    size = img[0].size
    i = -size/2
    flux_arr = []
    base = []
    linex = []
    liney = []
    while i < size/2:
        try:
            y = 1/np.tan(angle)*i+size/2
            x = (i + size/2)+offset
            liney.append(y)
            linex.append(x)
            flux = integ_inten(x, y, intrad, img)
            flux_arr.append(flux/norm)
            base.append((i+size/2)/np.sin(np.absolute(angle))-centering)
            i += 1
        except:
            break
    
    baseNorm = []
    for item in base:
        baseNorm.append(item/scale)
    print('here')
    if normalize == 'yes':
        flux_arr = flux_arr/(max(flux_arr))
    thefile = open('test.txt', 'w')
    for item in flux_arr:
        thefile.write(str(item)+',')
        #print(str(item))
    #print(flux_arr)
    #return(linex,liney)
    #print(flux_arr)
    return(baseNorm,flux_arr)
    
def mask(img, size, cutoff):
    j = 0
    while j < size:
        i = 0
        while i < size:
            if img[j][i] > cutoff:
                img[j][i] = 0
            i += 1
        j += 1
    return img

def fit(mass, tilt, rev):
    v = []
    G = 6.674E-11/(1E9)
    radius = 0.01*rev
    r = []
    mass = mass*2E30
    tilt = tilt*np.pi/180
    if rev == -1:
        while radius > -1000:
            v.append(np.sin(tilt)*np.sqrt(G * mass/(-radius*1.5E8))+5.5)
            r.append(radius)
            radius -= 0.1
    if rev == 1:
        while radius < 1000:
            v.append(-np.sin(tilt)*np.sqrt(G * mass/(radius*1.5E8))+5.5)
            r.append(radius)
            radius += 0.1
    return(r,v)    
'''hdus = fits.open('C:/Users/Somokai/Dropbox/Research/Data/gpi_HD100453_J_PI.fits_cropped.fits')
img1 = hdus[0].data

hdus = fits.open('C:/Users/Somokai/Dropbox/Research/Data/gpi_HD100453_Y_PI.fits_cropped.fits')
img2 = hdus[0].data

hdus = fits.open('C:/Users/Somokai/Dropbox/Research/Data/gpi_HD100453_K1_PI.fits_cropped.fits')
img3 = hdus[0].data'''

#hdu_list = fits.open('C:/Users/'+ usr +1'/Dropbox/Research/PDS70/Output/e_H2_52.0_0.0_I_img.fits')
hdu_list1 = fits.open(dir + 'continuum.fits')
#hdu_list2 = fits.open(dir + 'CO32_moment1.fits')
hdu_list2 = fits.open(dir + 'HCOp43_moment1.fits')
hdu_list3 = fits.open(dir + 'CO32_moment1.fits')
#hdu_list2 = fits.open('C:/Users/'+ usr +'/Dropbox/Research/PDS70/PDS70-ALMA-final2/continuum.fits')
#hdu_list3 = fits.open(dir + 'CO32_moment1.fits')
#hdu_list2 = fits.open(dir + 'continuum.fits')
#img1 = hdu_list1[0].data
img1 = hdu_list1[0].data
img2 = hdu_list2[0].data
img3 = hdu_list3[0].data

img1 = img1[0][0]
img2 = img2[0][0]
img3 = img3[0][0]
img1 = img1/0.0109835

#img = mask(img, 800, 300000)

#img = img1+img2+img3

#slice used
'''vslice = int(len(img)/2)
hslice = int(len(img)/2)
dslice = []'''


normY = 1
normJ = 1
normH = 1

fig, ax = plt.subplots()
#plt.imshow(img1, origin = 'lower')
#plt.colorbar()

#d_slice(-np.pi/4, img3, normY, 0, 60)
#vdata = v_slice(vslice, img, normY)
#hdata = h_slice(hslice, img, normY)
'''count = -5
while count < 5:
    d_slice(51/180*np.pi, img, 1, count*10, 0)
    count += 1'''

#d_slice(angle, img3, norm, offset,centering,scale,intrad, normalize)
#ddata1 = d_slice(21/180*np.pi, img1, 1, 42, 1301, 0.434, 1, 'yes')
ddata1 = d_slice(21.1/180*np.pi, img2, 1, 42, 1301, 0.434, 1, 'no')
ddata2 = d_slice(21.1/180*np.pi, img3, 1, 42, 1301, 0.434, 1, 'no')
#ax.plot(ddata1[0],ddata1[1], color = 'y')
#ddata2 = d_slice(21/180*np.pi, img2, 1, 40, 1307, 1, 10, 'yes')
#ddata3 = d_slice(21/180*np.pi, img3, 1, 42, 1307, 1, 1, 'no')
#plt.plot([0,0,0],[0,1,2])
#plt.plot((-100,100),(5.5,5.5),'k-')
#ddata2 = d_slice(-39/180*np.pi, img, 1, 0, 60)

'''vwriter = csv.writer(open(dir + "vdata.csv", 'w'))

vwriter.writerow(vdata)

hwriter = csv.writer(open(dir + "hdata.csv", 'w'))

hwriter.writerow(hdata)'''

#plt.xlim(-100, 100)
#plt.ylim(0,2000)
#plt.ylim(0,1.1)

imgFitL1 = fit(0.8, 45, -1)
imgFitU1 = fit(0.8, 45, 1)
plt.plot(imgFitL1[0], imgFitL1[1], color = 'k', linewidth = 2, linestyle='--')
plt.plot(imgFitU1[0], imgFitU1[1], color = 'k', linewidth = 2, linestyle='--')
plt.ylim(0, 12)
plt.xlim(-300, 300)
plt.plot(ddata2[0], ddata2[1])
plt.axvline(0, color = 'k', linestyle = 'dashed')
plt.axhline(5.48, color = 'k', linestyle = 'dashed')
plt.xlabel('Offset (AU)')
plt.ylabel('Velocity (km/s)')
plt.show()
imgFitL2 = fit(0.8, 45, -1)
imgFitU2 = fit(0.8, 45, 1)
plt.plot(imgFitL2[0], imgFitL2[1], color = 'k', linewidth = 2, linestyle='--')
plt.plot(imgFitU2[0], imgFitU2[1], color = 'k', linewidth = 2, linestyle='--')
plt.ylim(0, 12)
plt.xlim(-300, 300)
plt.axvline(0, color = 'k', linestyle = 'dashed')
plt.axhline(5.48, color = 'k', linestyle = 'dashed')
plt.plot(ddata1[0], ddata1[1])
plt.xlabel('Offset (AU)')
plt.ylabel('Velocity (km/s)')
plt.show()


'''plt.axvline(48, color = 'k', linestyle = 'dashed')
plt.axvline(60, color = 'k', linestyle = 'dashed')
plt.axvline(102, color = 'k', linestyle = 'dashed')
plt.axvline(-48, color = 'k', linestyle = 'dashed')
plt.axvline(-60, color = 'k', linestyle = 'dashed')
plt.axvline(-102, color = 'k', linestyle = 'dashed')'''


plt.show()
plt.axis('off')


'''blue_patch = mpatches.Patch(color='blue', label='Continuum')
green_patch = mpatches.Patch(color='green', label='HCOp43')
red_patch = mpatches.Patch(color='red', label='CO32')
plt.legend(handles=[blue_patch, green_patch, red_patch])'''
#img_scale('40 AU', (600,300), 19)
#plt.savefig(dir + 'Continuum_thing.png', dpi = 300)
#plt.show()