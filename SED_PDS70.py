import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.io.idl import readsav
import gzip
import numpy as np
import shutil
import os

comp = 'C:/Users/Somokai'
#comp = 'C:/Users/uberg'
#comp = '/Users/Zac'

#Stellar Parameters
rstar = 1.25
tstar = 4400
lumscale = 1
dis = 140
Av = 0.51 #reddening

#Preps the fits file for plotting, HOCHUNK3D uses zipped files
plt.clf()
dir = comp + '../Output/'
dirP = comp + ''
inF = gzip.GzipFile('../Output/peel_hypercube.fits.gz', 'rb')
s = inF.read()
inF.close()
outF = open('../Output/peel_hypercube.fits', 'wb')
outF.write(s)
outF.close()

hdu_list = fits.open('../Output/peel_hypercube.fits')
image_data = hdu_list[0].data
wavelength = hdu_list[1].data
flux = hdu_list[0].data
hdu_list.close()

sigma = 5.67e-5
pc = 3.0857e18
lsun = 3.845e33
fnorm = lumscale/(4*3.1416)/dis**2/pc**2*lsun/1e3

normFlux = flux[0][0][0][0]*fnorm
print(normFlux)

from astropy.io.votable import parse
votable = parse('../SED/vizier_votable.vot')

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

table = votable.get_first_table()
data = table.array

for d in data:
    #print(d)
    stored = str(d[7])
    #print(stored)
    stored = stored.strip("b'")
    #print(stored)
    stored = stored.split(":", 1)[0]
    #print(stored)
    if stored not in prevstored:
        prevstored.append(stored)
    if stored in data_processed.keys():
        data_processed[stored].append([3E5/d[4],(d[5]*3E-12)/(3E5/d[4]),(d[6]*3E-12)/(3E5/d[4])])
    else:
        data_processed[stored] = []
        data_processed[stored].append([3E5/d[4],(d[5]*3E-12)/(3E5/d[4]),(d[6]*3E-12)/(3E5/d[4])])




#fig, ax = plt.subplots()
#ax.set_color_cycle(['blue','green','red','magenta','cyan', 'black', 'purple'])


data = np.loadtxt('lte44-4.5-0.0.spec.ascii')
lumstar = 4*3.1416*(rstar*6.955e10)**2*sigma*tstar**4
rstar2 = lumstar/(4*3.1416*sigma)/tstar**4
atnorm = rstar2/dis**2/pc**2
print('atnorm is:' + str(atnorm))

xData = []
yData = []
for d in data:
    xData.append(d[0])
    yData.append(d[1]/d[0]*2.9929e14*atnorm/1000)


plt.plot(xData, yData,linestyle = 'dotted', color = 'blue')

keys = []
for key in data_processed.keys():
    keys.append(key)

#colors = ['#7d3c98','#5dade2','#17a589','#1d8348','#d4ac0d','#dc7633','#FF00FF', '#00FFFF','#FFFF00']
colors = ['aqua','chocolate','maroon','violet','indigo','goldenrod','lime', 'green','olive']
    
i = 0
for value in data_processed.values():
    xData = []
    yData = []
    yError = []
    yLims = []
    for d in value:
        xData.append(d[0])
        yData.append(d[1])
        #print(np.isnan(d[2]))
        if np.isnan(d[2]) == bool(0):
            yLims.append(bool(0))
            yError.append(d[2])
        else:
            yLims.append(bool(1))
            #print('masked')
            yError.append(.4*d[1])
    #plt.plot(xData, yData, 'o', label = keys[i])
    #print(keys[i],len(yError), len(yLims), yLims)
    plt.errorbar(xData, yData, yerr = yError, uplims = yLims, fmt = 'o', color = colors[i], label = keys[i])
    print(colors[i])
    i += 1

a = readsav('../SED/psd70_irs.sav')

point1 = [0.87*1E3, 34.01*3E-12/(0.87*1E6)]
#point1 = [0.87*1E3, 14.25*3E-12/(0.87*1E6)]
point2 = [1.3*1E3, 38.1*3E-12/(1.3*1E6)]



plt.plot(a.W_LL1, a.LFL_LL1,'r-', color = 'red', label = "Spitzer")
plt.plot(a.W_LL2, a.LFL_LL2,'r-', color = 'red')
plt.plot(a.W_SL1, a.LFL_SL1,'r-', color = 'red')
plt.plot(a.W_SL2, a.LFL_SL2,'r-', color = 'red')
plt.plot(point1[0], point1[1], 'bo', label = "ALMA")
plt.plot(point2[0], point2[1], 'go', label = "SMA")
#[3E5/d[4],(d[5]*3E-12)/(3E5/d[4]),(d[6]*3E-12)/(3E5/d[4])]

#print(point)


plt.plot(wavelength, normFlux,'black' )
plt.xscale('log')
plt.yscale('log')
plt.ylabel('$\lambda F_\lambda (W/m^2)$')
plt.xlabel('$\lambda (\mu m)$')
plt.legend(prop={'size':6})
plt.xlim(0.08,4500)
plt.ylim(10E-18,10E-13)
#test = dirP + "SED-Previous"
#os.remove(test)
shutil.copy2('SED-New.png', 'SED-Previous.png')
plt.savefig('SED-New.png', dpi = 300)
plt.show()
        
