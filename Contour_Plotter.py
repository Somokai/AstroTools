import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.ticker import FormatStrFormatter

#-----------------------Basic Parameters for Figure---------------------------#

#Images used, the background image is the one in full color, the contour image is overlaid
#on the other image.
backgroundImg = 'example1.fits'
contourImg = 'example2.fits'

#Color map of output image, for more color options go to:
#https://matplotlib.org/examples/color/colormaps_reference.html
backgroundColor = 'seismic'

#Color of the contour, simply put in reasonable color names
contourColor = 'black'

#Contour levels
levels = [0.0005, 0.0025, 0.0045, 0.0065, 0.0085]

#X and Y limits for the images
xL = 350
xH = 750
yL = 250
yH = 650

#Name of output image
imgName = 'output.png'


#---------------------Code Below for Advanced Changes------------------------#

hdu_list1 = fits.open(backgroundImg)
hdu_list2 = fits.open(contourImg)

img1 = hdu_list1[0].data
img2 = hdu_list2[0].data

def img_scale(text, loc, width):
    ax.text(loc[0]-14, loc[1]+5, text, color = 'w')
    ax.plot((loc[0], loc[0]+width),(loc[1],loc[1]), color = 'w', lw = 2)
    
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

#May need to change the array depending on the fits image
img1 = img1[0][0]
img2 = img2[0][0]

#Masking the contour image
'''img2 = mask(img2, 960, 50)'''

plt.axis('off')  
plt.imshow(img1, cmap = backgroundColor, vmin = 0, vmax = 11)

#Color bar information
'''plt.colorbar(format = '%.2f').set_label('Flux Density (mJy)')'''

plt.contour(img2, levels, colors = contourColor)

#Image Scale 
'''img_scale('40 AU', (600,300), 19)'''

plt.ylim(yL, yH)
plt.xlim(xL, xH)
plt.yticks()
plt.savefig(imgName, dpi = 300) 
plt.show()