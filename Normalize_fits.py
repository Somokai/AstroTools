# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 18:44:19 2016

@author: Somokai
"""

import pyfits


usr = 'Somokai'

y_img = pyfits.getdata('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Data/HIP56354_ifs_science_median_Y.fits')
j_img = pyfits.getdata('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Data/HIP56354_ifs_science_median_J.fits')
h_img = pyfits.getdata('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Data/HIP56354_ifs_science_median_H.fits')

y_imgh = pyfits.getheader('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Data/HIP56354_ifs_science_median_Y.fits')
j_imgh = pyfits.getheader('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Data/HIP56354_ifs_science_median_J.fits')
h_imgh = pyfits.getheader('C:/Users/'+ usr +'/Dropbox/Research/HD100453/Data/HIP56354_ifs_science_median_H.fits')

normY = 34.7
normJ = 35.7
normH = 43.7

y_img = y_img/normY
j_img = j_img/normJ
h_img = h_img/normH

pyfits.writeto('NormalizedY.fits', y_img, y_imgh)
pyfits.writeto('NormalizedJ.fits', j_img, j_imgh)
pyfits.writeto('NormalizedH.fits', h_img, h_imgh)