import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.convolution import convolve_fft, Gaussian2DKernel
import numpy as np
import scipy
from scipy import ndimage

#Image file, make sure you either have the path or run this in the correct folder
img = 'example.fits'

#X and Y limits of the deprojected image in pixels
xL = 300
xH = 500
yL = 0
yH = 150



def search(image, i, j):
    count = 0
    temp = 0
    while count < 10:
        if image[i][j-count] != 0:
            temp = image[i][j-count]
            break
        elif j + count < 960 and image[i][j+count] != 0:
            temp = image[i][j+count]
            break
        elif image[i-count][j] != 0:
            temp = image[i-count][j]
            break
        elif i + count < 960 and image[i+count][j] != 0:
            temp = image[i+count][j]
            break
        count += 1
    return temp
    
def fill(image):
    i = 0
    size = np.sqrt(image.size)
    filled = np.zeros((size, size))
    for row in image: 
        j = 0
        for column in row:
            if column == 0:
                column = search(image, i, j)                
            filled[i][j] = column
            j += 1
        i += 1
    return filled

def deproject(file, rot, tilt):
    size = np.sqrt(file.size)
    image = np.zeros((size,size))
    i = 1
    for row in file:
        j = 1
        for col in row:
            x = i*np.cos(np.pi/180.*rot) + j*np.sin(np.pi/180.*rot)
            y = -i*np.sin(np.pi/180.*rot) + j*np.cos(np.pi/180.*rot)
            #below I don't think is necessary actually
            '''z = np.sqrt(x*x+y*y/np.cos(np.pi/180*tilt)/np.cos(np.pi/180*tilt))
            phi = np.arctan(y/x)
            #nZ = z/np.cos(np.pi/180*tilt)
            nX = z*np.sin(phi)
            nY = z*np.cos(phi)
            #print(nX)
            if np.abs(nY) < size and np.abs(nX) < size:
                image[int(nY)][int(nX)] = file[i-1][j-1] '''        
            if np.abs(y/np.cos(tilt*np.pi/180)) < size and np.abs(x) < size:
                image[int(y/np.cos(tilt*np.pi/180))][int(x)] = file[i-1][j-1]
            
            j += 1
        i += 1
    image = fill(image)
    plt.figure()
    plt.imshow(image)
    return image

def scan_plot(image, center):
    size = np.sqrt(image.size)
    scan = np.zeros((size/2,size/2))
    j = 0
    while j < size/2:
        length = 0
        while length < size/2:
            x = np.cos(j*720/size*np.pi/180)*length
            y = np.sin(j*720/size*np.pi/180)*length
            if x*x + y*y < 350*350: 
                scan[length][j] = image[int(y+center[1])][int(x+center[0])]
            length += 1
        j += 1
    axis = [0, 90*480/360, 180*480/360, 270*480/360, 480]
    plt.figure()
    plt.imshow(scan, origin = 'lower')
    my_xticks = ['0','90','180','270', '360']
    plt.xticks(axis, my_xticks)
    plt.show


    

hdu_list = fits.open(img)
img = hdu_list[0].data

#Depending on the kind of fits image you are using this may need changed to a different array
img = img[0][0]

plt.figure()
plt.imshow(img, origin = 'lower')
image = deproject(img, 22, 45)
fill(image)
scan_plot(image, (607, 431))
plt.xlim(xL,xH)
plt.ylim(yL,yH)

plt.show()