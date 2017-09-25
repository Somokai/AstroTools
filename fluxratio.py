import glob
import gzip
from astropy.io import fits
import matplotlib.pyplot as plt


for file in glob.glob('../Output/*I_img.fits.gz'):
    inF = gzip.GzipFile(file, "rb")
    s = inF.read()
    inF.close()
    w = file
    w = str(w)
    
    print(w)
    w = w.replace('e_','')
    w = w.replace('_45.0_0.0_I_img.fits.gz','')
    outF = open('../Output/' + w + '_done.fits', 'wb')
    outF.write(s)
    outF.close()


flux = []
    
for file in glob.glob('../Output/*done.fits'):
    hdus = fits.open(file)
    total = 0
    img = hdus[0].data
    for row in img:
        rowsum = sum(row)
        total += rowsum
    fstar = img[399][399]+img[399][400]+img[400][399]+img[400][400]
    flux.append((total-fstar)/total)
    print(total, fstar)
    
wavelength = [1.2, 1.6, 2.2, 70, 110, 170, 250, 360, 520, 3.6, 4.5, 5.8, 8.0, 0, 24, 70, 160, 0, 0, 870, 0, 0, 0, 0]
print(len(wavelength))
print(len(flux))
  
plt.plot(wavelength, flux, 'o')
plt.xscale('log')
plt.ylim(0, 1.1)
plt.ylabel('$F_{disk}/F_{total}$')
plt.xlabel('$\lambda (\mu m)$')
#plt.yscale('log')
plt.show()