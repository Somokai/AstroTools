import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.io.idl import readsav
import gzip
import numpy as np
import shutil
import os
from astropy.io.votable import parse

'''This script can work with Vizier .vot files, you can get these after looking up your star on 
SIMBAD. You can also include various other data that is used as long as you explicitly include those.
The extra data can be included towards the bottom of the file.'''

#-----------------------Basic Parameters for Figure---------------------------#

#Path to model SED file (generally located in Output)
dir = '../Output/'

#Stellar Parameters
rstar = 1.25        #radius of the star in solar radii
tstar = 4400        #temperature of the star in K
lumscale = 1        #luminosity scale, generally just set to 1
dis = 140           #distance to the star in parsecs
Av = 0.51           #reddening

#SED Data
dirSED = '../SED/'   #path to the SED Data

#Votable Data for SED    
votableFile = 'yes' #if you have a votable file make sure to set this to yes, put it in the same file path
                    #as the rest of your SED data
                    
#Colors of Votable Data it will cycle through these colors by default
colors = ['aqua','chocolate','maroon','violet','indigo','goldenrod','lime', 'green','olive']                    
                 

#X and Y Limits of the plot, intensity (lambda/Flambda) for y and wavelength (micron) for x
xL = 0.08 
xH = 4500
yL = 10E-18
yH = 10E-13

#Photospheric file
photFile = 'lte44-4.5-0.0.spec.ascii'
 
 
#---------------------Code Below for Advanced Changes------------------------#                   
                    
                    
#Preps the fits file for plotting, HOCHUNK3D uses zipped files
plt.clf()
inF = gzip.GzipFile(dir + 'peel_hypercube.fits.gz', 'rb')
s = inF.read()
inF.close()
outF = open(dir + 'peel_hypercube.fits', 'wb')
outF.write(s)
outF.close()

hdu_list = fits.open(dir + 'peel_hypercube.fits')
image_data = hdu_list[0].data
wavelength = hdu_list[1].data
flux = hdu_list[0].data
hdu_list.close()

#Constants used in calibration
sigma = 5.67e-5
pc = 3.0857e18
lsun = 3.845e33
fnorm = lumscale/(4*3.1416)/dis**2/pc**2*lsun/1e3

normFlux = flux[0][0][0][0]*fnorm

data_processed = {}
prevstored = []

klam = []
kkap = []

with open ('kmhnew_extrap.par') as file:
    for line in file:
        line = line.split()
        klam.append(line[0])
        kkap.append(line[3])

waveNew = []
for item in wavelength:
    w = item
    w = str(w)
    w = list(w)
    w.remove('(')
    w.remove(')')
    w = "".join(w)
    w = float(w)
    waveNew.append(w)
    
        
kapnew = np.interp(waveNew, klam, kkap)
kapv = np.interp(0.55, klam, kkap)
taul = kapnew/kapv/1.086*Av
extinct = np.exp(-taul)

normFlux = normFlux*extinct

if votableFile == 'yes' or votableFile == 'Yes' or votableFile == 'y':
    votable = parse(dirSED + 'vizier_votable.vot')
    table = votable.get_first_table()
    data = table.array

    for d in data:
        stored = str(d[7])
        stored = stored.strip("b'")
        stored = stored.split(":", 1)[0]
        if stored not in prevstored:
            prevstored.append(stored)
        if stored in data_processed.keys():
            data_processed[stored].append([3E5/d[4],(d[5]*3E-12)/(3E5/d[4]),(d[6]*3E-12)/(3E5/d[4])])
        else:
            data_processed[stored] = []
            data_processed[stored].append([3E5/d[4],(d[5]*3E-12)/(3E5/d[4]),(d[6]*3E-12)/(3E5/d[4])])

    keys = []
    for key in data_processed.keys():
        keys.append(key)
    
    i = 0
    for value in data_processed.values():
        xData = []
        yData = []
        yError = []
        yLims = []
        for d in value:
            xData.append(d[0])
            yData.append(d[1])
            if np.isnan(d[2]) == bool(0):
                yLims.append(bool(0))
                yError.append(d[2])
            else:
                yLims.append(bool(1))
                yError.append(.4*d[1])
        plt.errorbar(xData, yData, yerr = yError, uplims = yLims, fmt = 'o', color = colors[i], label = keys[i])
        print(colors[i])
        i += 1
        
    

photData = np.loadtxt(photFile)
lumstar = 4*3.1416*(rstar*6.955e10)**2*sigma*tstar**4
rstar2 = lumstar/(4*3.1416*sigma)/tstar**4
atnorm = rstar2/dis**2/pc**2

xData = []
yData = []
for d in photData:
    xData.append(d[0])
    yData.append(d[1]/d[0]*2.9929e14*atnorm/1000)

plt.plot(xData, yData, linestyle = 'dotted', color = 'blue')

#----------------------------Extra Data Input--------------------------------#

#Example of how you might include some data
'''a = readsav(dirSED + '/idlSaveFile.sav')
plt.plot(a.W_LL1, a.LFL_LL1,'r-', color = 'color', label = "DataName")
plt.plot(a.W_LL2, a.LFL_LL2,'r-', color = 'colro')
plt.plot(a.W_SL1, a.LFL_SL1,'r-', color = 'color')
plt.plot(a.W_SL2, a.LFL_SL2,'r-', color = 'color')'''

#----------------------------Making the Image--------------------------------#

plt.plot(wavelength, normFlux,'black' )
plt.xscale('log')
plt.yscale('log')
plt.ylabel('$\lambda F_\lambda (W/m^2)$')
plt.xlabel('$\lambda (\mu m)$')
plt.legend(prop={'size':6})
plt.xlim(xL, xH)
plt.ylim(yL, yH)
plt.savefig('SED.png', dpi = 300)
plt.show()
        
