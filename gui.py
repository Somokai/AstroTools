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

class Application(Frame):
    
    def __init__(self, master):
        #initialized the frame
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        
        
    
    def create_widgets(self):
        #create buttons that do nothing right now

        self.button1 = Button(self, text = "Choose File")
        self.button1["command"] = self.load_fits
        self.button1.grid()
        
        self.canvas = Canvas(root, width=canvas_width, height=canvas_height)
        self.message = Label(self)
        self.message["text"] = "Choose Fits File"
        self.message.grid()
        

    
    def load_fits(self):
        #increase the click count and display new total
        filename = filedialog.askopenfilename(filetypes = (("Fits files", "*.fits")
                                                             ,("All files", "*.*") ))
        print(filename)
        self.img_canvas(filename)
    
    def img_manip(self,filename):
        hdus = fits.open(filename)
        global image 
        image = hdus[0].data
        fig,ax = plt.subplot(1)
        fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
        img = plt.imshow(image, origin = "lower")
        .subplots_adjust(left=0,right=1,bottom=0,top=1)
        plt.axis('off')
        plt.savefig(filename[:-5]+'.png', bbox_inches='tight')
        imgNew = PhotoImage(file = filename[:-5]+'.png')
        self.imgNew = PhotoImage(file = filename[:-5]+'.png')
        self.message["text"] = "Click on Center of Object"
        self.canvas.bind("<Button-1>", self.select)
        
        
        
        
    def select(self, event):
        x, y = ( event.x - 1 ), ( event.y - 1 )
        center = (x,y)
        print(center)
        #self.center_plot(center)
        
    def center_plot(self, center):
        newCenter = find_center(center, image)
        print(newCenter)
        circ = circle_oplot(10, newCenter)
        plt.plot(circ[0], circ[1], 'y')
        plt.show()
    
#create the window
root = Tk()

#modify root window
root.title('Fits Image Manipulator')
root.geometry('900x800')

app = Application(root)


#kick off the main loop
root.mainloop()

