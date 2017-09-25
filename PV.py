import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

def integ_inten(x,y,r,img):
    row = 0
    flux = 0
    temp = r
    while row < r:
        i = 0
        while i < 2*temp-1:
            flux = flux + img[(y-temp+i),(x+row)]
            #print((y-temp+i),(x+row),flux)
            if row > 0:
                flux = flux + img[(y-temp+i),(x-row)]
            i += 1
        row += 1
        temp -= 1
    return flux

def d_slice(angle, img, norm, offset,centering,scale,intrad, normalize):
    flux = 0
    size = img[0].size
    i = -100
    flux_arr = []
    base = []
    while i < 400:
        try:
            y = 1/np.tan(angle)*i+size/2
            x = (i + size/2)+offset
            flux = integ_inten(x, y, intrad, img)
            flux_arr.append(flux/norm)
            base.append((i+size/2)/np.sin(np.absolute(angle))-centering)
            #print(i)
            i += 1
        except:
            break
    
    baseNorm = []
    for item in base:
        baseNorm.append(item/scale)
    if normalize == 'yes':
        flux_arr = flux_arr/(max(flux_arr))
    thefile = open('test.txt', 'w')
    for item in flux_arr:
        thefile.write(str(item)+',')
        #print(str(item))
    #print(flux_arr)
    return(baseNorm, flux_arr)

def fit(mass, tilt, rev):
    v = []
    G = 6.674E-11/(1E9)
    radius = 0.01*rev
    r = []
    mass = mass*2E30
    tilt = tilt*np.pi/180
    if rev == 1:
        while radius < 88:
            v.append(np.sin(tilt)*np.sqrt(G * mass/(radius*2.1*1.5E8))/0.211+72.5)
            #print(np.sin(tilt)*np.sqrt(G * mass/(radius*1.5E8)))
            r.append(radius+88)
            radius += 0.1

    else:
        while radius > -88:
            v.append(-np.sin(tilt)*np.sqrt(G * mass/(-radius*2.1*1.5E8))/0.211+72.5)
            #print(np.sin(tilt)*np.sqrt(G * mass/(-radius*2.1*1.5E8)),radius)
            r.append(radius+88)
            radius -= 0.1
    return(r,v)

    
hdu_list = fits.open('pds70cube/calibrated.ms.contsub.CO32_final.fits')
img = hdu_list[0].data
img = img[0]
#print(img)

 
i = 0 
image = []
while i < 139:    
    data = d_slice(21/180*np.pi, img[i], 1, 42, 1301, 1, 1, 'no')
    image.append(data[1])
    i += 1

imgFitL1 = fit(0.8, 40, 1)
imgFitU1 = fit(0.8, 40, -1)

imgFitL2 = fit(0.6, 40, 1)
imgFitU2 = fit(0.6, 40, -1)

imgFitL3 = fit(1.1, 40, 1)
imgFitU3 = fit(1.1, 40, -1)

#print(image)
fig, ax = plt.subplots()

linex = []
liney = []
i = 0
while i < 200:
    liney.append(-1/6*i + 120)
    linex.append(i)
    i += 1
  
ax.imshow(image, origin = 'lower')
ax.plot(imgFitL1[0], imgFitL1[1], color = 'w', linewidth = 2, linestyle='--')
ax.plot(imgFitU1[0], imgFitU1[1], color = 'w', linewidth = 2, linestyle='--')
ax.plot(imgFitL2[0], imgFitL2[1], color = 'r', linewidth = 2, linestyle='--')
ax.plot(imgFitU2[0], imgFitU2[1], color = 'r', linewidth = 2, linestyle='--')
ax.plot(imgFitL3[0], imgFitL3[1], color = 'k', linewidth = 2, linestyle='--')
ax.plot(imgFitU3[0], imgFitU3[1], color = 'k', linewidth = 2, linestyle='--')
#ax.plot(linex, liney)
#plt.axvline(x=88, color = 'w')
#plt.axhline(y=72.5, color = 'w')

plt.xlim(7,170)
plt.ylim(0,138)

#plt.xticks([])
plt.xticks([12.8, 31.6, 50.4, 69.2, 88, 106.8, 125.4, 144.4, 164.2])
ax.set_xticklabels([-200, -150, -100, -50, 0, 50, 100, 150, 200])
plt.xlabel('Offset (AU)')
plt.yticks([11.8, 26, 40.2, 54.3, 68.5, 82.7, 96.8, 111, 125.1])
ax.set_yticklabels([-12, -9, -6, -3, 0, 3, 6, 9, 12])
plt.ylabel('Velocity (km/s)')

plt.savefig('dynamical_fit.png', dpi = 300)
plt.show()