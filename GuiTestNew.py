from tkinter import *
from tkinter import filedialog
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import cm
import matplotlib
from astrotools import find_center
from astrotools import circle_oplot



def load_fits():
    #increase the click count and display new total
    global filename
    filename = filedialog.askopenfilename(filetypes = (("Fits files", "*.fits")
                                                         ,("All files", "*.*") ))
    display(filename)
    
def display(filename):
    hdus = fits.open(filename)
    global image
    image = hdus[0].data
    plt.imshow(image, origin = "lower")
    plt.show()
    #message["text"] = "Click on Center of Object"
    #canvas.bind("<Button-1>", select)
    
def select(event):
    x, y = ( event.x - 1 ), ( event.y - 1 )
    center = (x,y)
    print(center)
    #center_plot(center)
    




root = Tk()

#modify root window
root.title('Fits Image Manipulator')
root.geometry('200x400')

app = Frame(root)
app.grid()

message = Label()
message["text"] = "Choose Fits File"
message.grid()

button1 = Button(text = "Open File")
button1["command"] = load_fits
button1.grid()

button2 = Button(text = "Plot Circle")
button2["command"] = lambda:center_plot((464,496), image)
button2.grid()




#kick off the main loop
root.mainloop()



select(event)


