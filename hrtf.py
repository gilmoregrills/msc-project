import numpy as np
import os.path

#to do: 
#add method to print hrtf data in a useful way - similar to matlab
#add method to return hrtf data as graph/visualised usefully
#add get/set methods to inputroot and outputroot
#fix writeraw method to correctly write files
#add edit method to access specific array index and change value
#ensure all this is usable through jupyter notebooks
#set root paths in constructor
#set up rounding up/down for the input elev/azim

np.set_printoptions(threshold=np.inf)
#line above allows you to print all lines of hrf to the terminal

class hrtf: 
    'Class holding hrtf data array, input and output paths'

    data = None
    #hardcoded now, for personal use
    inputroot = "/home/gilmoregrills/hrtf-tests/MIT"
    outputroot = "/home/gilmoregrills/hrtf-tests/modified"

    #constructor, calls readraw and assigns the return to
    #the data variable
    def __init__(self, elev, azim, select):
        self.data = self.readraw(elev, azim, select)
    
    #used to send an hrtf array to the data variable
    #called on instantiation, uses input root
    def readraw(self, elev, azim, select):
        root = self.inputroot
        dt = np.dtype('>i2')
    
        #checks the azimuth/elevation value is valid
        if (azim < 0) or (azim > 180):
            print('azimuth must be between 0 and 180 degrees')
        elif (elev < -40) or (elev > 90):
            print('azimuth must be between 0 and 180 degrees')
 
        #creates the flipazim variable based on azim above
        flipazim = 360 - azim
        if (flipazim == 360):
            flipazim = 0

    #selects the file to be accessed, depending on value of select
    #returns it as a 2/512 array holding data for L/R
        if (select == 'L'):
            pathname = self.hrtfpath(root,'full',select,elev,azim)
            larray = np.fromfile(pathname, dt, -1, "")
            pathname = self.hrtfpath(root,'full',select,elev,flipazim)
            rarray = np.fromfile(pathname, dt, -1, "")
            outputarray = np.vstack((larray, rarray))
            return(outputarray)
        elif (select == 'R'):
            pathname = self.hrtfpath(root,'full',select,elev,flipazim)
            larray = np.fromfile(pathname, dt, -1, "")
            pathname = self.hrtfpath(root,'full',select,elev,azim)
            rarray = np.fromfile(pathname, dt, -1, "")
            outputarray = np.vstack((larray, rarray))
        elif (select == 'H'):
            #nothing here yet
	    print("this isn't a thing yet")
        else:
            print("something went wrong")

        return(outputarray)
    
    #not fully working, needs to split the array into two halves
    #and write to different files, but the basics are there
    def writeraw(hrtfarray, elev, azim, select):
        subdir = "full"
        root = self.outputroot
        writepath = hrtfpath(root, subdir, select, ".dat", elev, azim)
        hrtfarray.tofile(writepath)

    #just returns as a string the filepath to the hrtf that
    #needs accessing
    def hrtfpath(self, root, subdir, select, elev, azim):
        x = '/'
        ext = '.dat'
        return(root+x+subdir+x+"elev"+str(elev)+x+select+str(elev)+"e"+str(azim)+"a"+ext) 
