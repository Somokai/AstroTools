import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


hdu_list1 = fits.open('../PDS70-ALMA-final2/CO32_moment1.fits')
img = hdu_list1[0].data
img = img[0][0]

i = 0
newImg = np.zeros((960,960))
'''while i <  950:
    liney.append(-1/2 * i + 703)
    linex.append(i)
    i += 1'''

sort = []
i = 0
while i < 960:
    sort.append(i*20/960)
    i += 1

def function(image, y, x):
    z = 0
    while z < 960:
        if image[y][x] >= sort[z] and image[y][x] < sort[z+1]:
            newImg[z][y]
            break
        z += 1    
        
i = 0        
while i < 960:
    j = 0
    while j < 960:
        function(img, i, j)
        j += 1
    i += 1
    print(i)
    
print(newImg)    
plt.imshow(newImg, origin = 'lower')
#plt.scatter(linex,liney, linewidths = 1)

#plt.ylim(250, 650)
#plt.xlim(300, 700)

plt.show()