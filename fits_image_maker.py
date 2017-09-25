# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 17:57:05 2016

@author: uberg
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits

dir = ('C:/Users/Somokai/Dropbox/Research/HD100453/Plots/Fits_Images_PA_220/Mis_45_1.38_Outer_flare/')


hdu_list1 = fits.open(dir + 'e_IH_25.0_220.0_I_img_convolved.fits')
image_data1 = hdu_list1[0].data
hdu_list1.close()
hdu_list2 = fits.open(dir + 'e_IJ_25.0_220.0_I_img_convolved.fits')
image_data2 = hdu_list2[0].data
hdu_list2.close()
hdu_list3 = fits.open(dir + 'e_IY_25.0_220.0_I_img_convolved.fits')
image_data3 = hdu_list3[0].data
hdu_list3.close()


image_data = image_data1 + image_data2 + image_data3

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim(0,300)
plt.xlim(0,300)
#plt.plot([128, 165], [95, 95], 'k-', lw=2)
#ax.annotate('0.3"', xy=(130,220 ), xytext=(141, 85))
plt.axis('off')
#plt.plot(image_data)
plt.imshow(image_data, cmap='spectral')
#fig.savefig('C:/Users/uberg/Dropbox/Research/image.png')