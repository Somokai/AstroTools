import matplotlib.pyplot as plt
from astropy.io import fits
import gzip
import matplotlib.gridspec as gridspec


rmax1 = 2
rmax2 = 80
rmax3 = 125

dir = 'C:/Users/Somokai/Dropbox/Research/PDS70/Output/'

rhoamb = 0

minT = 10
maxT = 1600


inF = gzip.GzipFile(dir + 'tarr.fits.gz', 'rb')
s = inF.read()
inF.close()
outF = open(dir + 'tarr.fits', 'wb')
outF.write(s)
outF.close()

inF = gzip.GzipFile(dir + 'darr.fits.gz', 'rb')
s = inF.read()
inF.close()
outF = open(dir + 'darr.fits', 'wb')
outF.write(s)
outF.close()

temp = fits.open(dir + 'tarr.fits')
tempImg = temp[0].data
tempImg = tempImg[0][0]+tempImg[1][0]+tempImg[2][0]+tempImg[3][0]


den = fits.open(dir + 'darr.fits')
denImg = den[0].data
denImg = denImg[0][0]+denImg[1][0]+denImg[2][0]+denImg[3][0]
denImg1 = denImg[0:2]


fig = plt.figure()

ax1 = fig.add_subplot(2,3,1)
ax2 = fig.add_subplot(2,3,2)
ax3 = fig.add_subplot(2,3,3)
ax4 = fig.add_subplot(2,3,4)
ax5 = fig.add_subplot(2,3,5)
ax6 = fig.add_subplot(2,3,6)

ax1.imshow(denImg, aspect = 'auto')
ax1.set_xlim([0,20],)
ax2.imshow(denImg, aspect = 'auto')
ax2.set_xlim([0,200])
ax3.imshow(denImg, aspect = 'auto')
ax3.set_xlim([0,399])
ax4.imshow(tempImg, aspect = 'auto')
ax4.set_xlim([0,20],)
ax5.imshow(tempImg, aspect = 'auto')
ax5.set_xlim([0,200])
ax6.imshow(tempImg, aspect = 'auto')
ax6.set_xlim([0,399])
plt.tight_layout()

plt.savefig('C:/Users/Somokai/Dropbox/Research/PDS70/TD.png', dpi = 300)
#plt.imshow(tempImg, extent = [0,1,0,2])

#plt.imshow(denImg[0][0]+denImg[1][0]+denImg[2][0]+denImg[3][0])
plt.draw
plt.show()
