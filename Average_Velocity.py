import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

#Image file being used
img = 'example.fits'

#Diagonal 
diagonal = 600

hdu_list = fits.open(img)
img = hdu_list[0].data

#-----------------------------Code Below---------------------------------#

#May need to be changed to a different array depending on the fits file.
img = img[0][0]

#Initialization of the variables
total = 0
count = 0
t = 0
i = -diagonal/2
j = -diagonal/2

#Loop tries to find the average velocity, you may need to change the number of loops you have
while i < 480:
    if np.sqrt(i*i+j*j) < diagonal/2:
        total += img[i+450][j+450]
        t += img[i+450][j+450]
        print(t)
        count += 1
        print(count)
    i += 1
    j += 1


print(total/count)