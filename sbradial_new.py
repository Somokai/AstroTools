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
        x = (x1+center2[0])  
        y = (y1+center2[1])
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


#usr = 'Somokai'
usr = 'uberg'


    
#hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/Data/HIP56354_ifs_science_median_Y.fits')
#img1 = hdus[0].data

hdus = fits.open('../PDS70-ALMA-final2/continuum.fits')
#hdus = fits.open('../PDS70-ALMA-final2/pds70.cont.image.pbcor.fits')
img1 = hdus[0].data

'''hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/e_IJ_25.0_220.0_I_img_convolved.fits')
img2 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/Data/HIP56354_ifs_science_median_H.fits')
img3 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/Data/HIP56354-flux-calib_K1_median.fits')
img4 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/Data/HIP56354_ird_science_median_K2.fits')
img5 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/e_2J_38.0_242.0_I_img_convolved.fits')
img6 = hdus[0].data'''

'''hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Final_Model/e_IH_25.0_220.0_I_img.fits')
img6 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_1.0_flare/e_IH_25.0_220.0_I_img.fits.gz')
img7 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_1.0_flare/e_IH_25.0_220.0_PF_img.fits.gz')
img8 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_1.0_flare/e_IH_25.0_220.0_I_img.fits.gz')
img9 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_1.0_flare/e_IH_25.0_220.0_I_img.fits.gz')
img10 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_Z_0.9/e_IH_25.0_220.0_I_img_convolved.fits')
img11 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_Z_1.0/e_IH_25.0_220.0_I_img_convolved.fits')
img12 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_Z_1.1/e_IH_25.0_220.0_I_img_convolved.fits')
img13 = hdus[0].data

hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Data/gpi_HD100453_Y_PI.fits_cropped.fits')
img16 = hdus[0].data'''

#hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/Data/gpi_HD100453_J_PI.fits_cropped.fits')
img14 = hdus[0].data

#hdus = fits.open('C:/Users/'+ usr +'/Dropbox/Research/Data/gpi_HD100453_K1_PI.fits_cropped.fits')
img15 = hdus[0].data

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 30}

matplotlib.rc('font', **font)


#integration radius
intrad1 = 2
intrad2 = 4
intrad3 = 2

#center for these images is [y,x] for some reason
center1 = [145,145]
center2 = [150,151]
center3 = [109.5,109.5]
#center13 = [img13.shape[0]/2,img13.shape[1]/2]
center14 = [img14.shape[0]/2,img14.shape[1]/2]
center15 = [img15.shape[0]/2,img15.shape[1]/2]
#a and b are in pixels
a1 = 26
b1 = 21.5
a2 = 54
b2 = 49
a3 = 16
b3 = 13.2
a4 = 54
b4 = 42

#rotation of the ellipse
th1 = 45*np.pi/180

#normalization factor
normY = 35.8
normJ = 36.1
normH = 43.4
normK1 = 295.4*0.837/1.4
#
'''tilted_ring(img1, th1, center1, a1, b1, intrad1, normY, 0)
tilted_ring(img2, th1, center1, a1, b1, intrad1, normJ, 0)
tilted_ring(img3, th1, center1, a1, b1, intrad1, normH, 0)'''
#tilted_ring(img4, th1, center3, a3, b3, intrad3, normK1, 50)
#tilted_ring(img5, th1, center3, a3, b3, intrad3)
#tilted_ring(img13, th1, [center13[1], center13[0]], 13.5, 10.5, intrad1, 820, 0)
#tilted_ring(img14, th1, [center14[1], center14[0]], 13.5, 10.5, intrad1, 738, 0)
#tilted_ring(img15, th1, [center15[1], center15[0]], 13.5, 10.5, intrad1, 1175, 0)'''

#plt.imshow(img15,origin='lower')

'''pointx = []
pointy = []
tilted_ring_oplot(img15, th1, center15, 14, 11, intrad1)
plt.plot(pointx,pointy,'r')'''


'''pointx = []
pointy = []
tilted_ring_oplot(img13, th1, [40,40.5], 13.5, 10.5, 1)
plt.plot(pointx,pointy,'r')
plt.imshow(img13, origin = 'lower', cmap = cm.Blues_r, vmin = 1, vmax = 200)'''

img1 = img1[0][0]
#print(img1)          

centerI = (496,464)

#back_subtract(200,100,50,0,img1,(496,464),960)
back_subtract(300,200,100,0,img1,(510,451),960)
#back_subtract(39,30,28,8.5,img14,(43,41),82)
#back_subtract(110,90,85,30,img6,299)
#back_subtract(60,45,20,0,img2,280)

#pointx = []
#pointy = []
#ring_oplot(img6,center2,a2,b2,intrad2)
#plt.plot(pointx,pointy,'r')
'''pointx = []
pointy = []
ring_oplot(img6,center2,a2,b2,intrad2)
plt.plot(pointx,pointy,'r')

ring_oplot(img9,center2,56,47,intrad2)
plt.plot(pointx,pointy,'r')
pointx = []
pointy = []
ring_oplot(img9,center2,58.8,49.1,intrad2)
plt.plot(pointx,pointy,'r')
pointx = []
pointy = []
ring_oplot(img9,center2,61.7,51.8,intrad2)
plt.plot(pointx,pointy,'g')'''
#plt.imshow(img6, origin ='lower')
#plt.xlim(80,140)
#plt.ylim(80,140)

'''horizontal_ring(img6, center2, 48, 40.3, intrad2, normH)
horizontal_ring(img7, center2, 53.2, 44.7, intrad2, normH)
horizontal_ring(img8, center2, 56, 47, intrad2, normH)
horizontal_ring(img9, center2, 58.8, 49.4, intrad2, normH)
horizontal_ring(img10, center2, 61.7, 51.8, intrad2, normH)'''



#horizontal_ring(img6,center2,a4,b4,intrad2,1)
#horizontal_ring(img2,center2,a2,b2,intrad2,1)
'''horizontal_ring(img9,center2,a2,b2,intrad2,1)
horizontal_ring(img10,center2,a2,b2,intrad2,1)
horizontal_ring(img11,center2,a2,b2,intrad2,1)
horizontal_ring(img12,center2,a2,b2,intrad2,1)
horizontal_ring(img12,center2,a2,b2,intrad2,1)'''

#plt.plot(pointx,pointy)
#plt.imshow(img2)
'''blue_patch = mpatches.Patch(color='blue', label='GPI\nJ-Band\nImage')
green_patch = mpatches.Patch(color='green', label='Benisty\nModel\nRecreation')
red_patch = mpatches.Patch(color='red', label='Our\nBest Fit\nModel')
cyan_patch = mpatches.Patch(color='cyan', label='0.112 AU')
magenta_patch = mpatches.Patch(color='magenta', label='0.126 AU')
black_patch = mpatches.Patch(color='black', label = '0.140 AU')
yellow_patch = mpatches.Patch(color='yellow', label = '1.1')
plt.legend(handles=[blue_patch, green_patch, red_patch], fontsize = 24, loc = (0.8, 0.1))#, cyan_patch, magenta_patch,black_patch])#, black_patch])
plt.xlabel('Angle from North (\u00B0)')
plt.ylabel('Intensity (arbitrary units)')
'''
plt.xlim(375, 600)
plt.ylim(350, 600)
plt.imshow(img1)
plt.show()
plt.draw()
#plt.savefig('C:/Users/'+ usr +'/Dropbox/Research/plot.png')