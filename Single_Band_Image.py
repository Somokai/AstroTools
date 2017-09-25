import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.convolution import convolve_fft, Gaussian2DKernel
import numpy as np
import scipy
import scipy.ndimage
from matplotlib.patches import Ellipse
import matplotlib.colors as colors

#-----------------------Basic Parameters for Figure---------------------------#

#Image to be plotted
img = 'example1.fits'

#Color map of output image, for more color options go to:
#https://matplotlib.org/examples/color/colormaps_reference.html
colorMap = 'jet' 

#Convolution parameters.
convolve = 'no'     #whether or not to use convolution
conMaj = 100        #major axis of beam size
conMin = 150        #minor axis of beam size
conRot = 15         #rotation angle of beam in degrees

#Masking Parametes
masking = 'no'      #whether or not to use convolution
maskLevel = 1000    #any pixels brighter than this number will be set to zero

#Name of output image
imgName = 'output.png'

#---------------------Code Below for Advanced Changes------------------------#
'''There are many other functions that can be used for image manipulation included
in this file. For those who would like to use them make sure to read the descriptions
or simply ask me either in person or via email at longzc@mail.uc.edu'''

#Convolves the image with a provided beam shape
def convolve_img(img, size, sizey, rot):
    size = int(size)
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)
    x, y = scipy.mgrid[-size:size+1, -sizey:sizey+1]
    g = scipy.exp(-(x**2/float(size)+y**2/float(sizey)))
    g = scipy.ndimage.interpolation.rotate(g, rot)
    z = convolve_fft(img, g)
    return z

#Integrates all of the pixels within a given radius surrounding a central pixel
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
    
#Crops an image to a smaller size centered at the center of the image file
def remove_extra(image, size, max):
    i = size
    j = size
    new_image = []
    while  i < max - size:
        j = size
        temp_image = []
        while j < max - size:
            temp_image.append(image[i][j])
            j += 1
        new_image.append(temp_image)
        i += 1
    return new_image
    
#Squares the value of each pixel    
def squared(img, norm, size):
    j = 0    
    while j < size:
        i = 0
        while i < size:             
            img[j][i]=np.square(img[j][i]/norm)
            i += 1
        j += 1        
    return img

#Multiplies the intensity of a pixel based on it's distance from the center of the disk    
def r_squared(img, norm, size, inc,rot):
    j = 0
    while j < size:
        i = 0
        while i < size:
            r = 1 + np.absolute(np.cos(3.14159*rot/180+np.arccos(np.absolute(size/2-j)/np.sqrt((np.square(size/2-i)+np.square(size/2-j)))))*(1-1/np.cos(inc*3.14159/180)))
            img[j][i]=np.square(np.sqrt((np.square(size/2-i)+np.square(size/2-j)))*r)*img[j][i]/norm  
            i += 1
        j += 1
    return img

#Sets pixels below a certain threshold to zero  
def remove_background(image, size, cutoff):
    j = 0
    while j < size:
        i = 0
        while i < size:
            if image[j][i] < cutoff:               
                image[j][i] = 0
            i += 1
        j += 1
    return img

#Sets pixels above a certain threshold to zero
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

#Plots a diagonal slice of the given image 
def d_slice(angle, img, offset, centering, scale, xLim):
    flux = 0
    size = img[0].size
    i = -size/2
    x = []
    y = []
    flux_arr = []
    base = []
    while i < size:
        pointy = 1/np.tan(angle)*i+size/2
        pointx = (i + size/2)+offset
        x.append(pointx)
        y.append(pointy)
        try:
            flux = img[pointy, pointx]
            flux_arr.append(flux)
            base.append((i+centering)*scale)
        except:
            break
        i += 1
    plt.xlim(-xLim, xLim)
    plt.xlabel('Radius (AU)')
    plt.ylabel('Intensity (arb)')
    norm = max(flux_arr)
    plt.plot(base, flux_arr)
    return [x,y]

#Returns a horizontal slice of a given image    
def h_slice(slice, img, norm):
    plt.plot(img[slice-1]/norm)
    return(img[slice-1]/norm)

#Plots line and text showing the scale of the image
def img_scale(text, loc, width):
    ax.text(loc[0]-10, loc[1]+5, text, color = 'white')
    ax.plot((loc[0], loc[0]+width),(loc[1],loc[1]), color = 'white', lw = 2)


    
#-----------------------------------------------------------------------------#    
    
hdu_list = fits.open(img)
img = hdu_list[0].data
       
if masking == 'yes' or masking == 'Yes' or masking == 'y';
    img = mask(img, img[0].size, maskLevel)

if convolve == 'yes' or convolve == 'Yes' or convolve == 'y';
    img = convolve_img(img, conMin, conMaj, conRot)
    
fig, ax = plt.subplots()
cax = ax.imshow(img, origin = 'lower', cmap = colorMap)

#Optional Beam Size Plotter
'''e = Ellipse((10,10), 10, 10, angle = 15)
ax.add_artist(e)
e.set_facecolor('white')'''

fig.colorbar(cax, orientation = 'vertical')
plt.axis('off')
plt.savefig(imgName, dpi = 300)

plt.show()