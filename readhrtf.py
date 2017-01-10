import numpy as np
import os.path
np.set_printoptions(threshold=np.inf) 
#the above line allows you to print >100 lines to term

def readhrtf(elev, azim, select):
#elev = elevation, from 0 to 90 degrees
#azim = azimuth from 0 to 180 degrees
#select can be either: 
#   'L' for data from left pinna
#   'R' for data from right pinna
#   'H' for compact data
#
#original script stolen from Bill Gardner, all props to him
#and the MIT Media Lab

#takes the args and uses them to find the correct 
#hrtf from the MIT lib, then sorts it into a 2D
#array where row1 is always L and row2 is always R
def readraw(elev, azim, select):
    root = '/home/gilmoregrills/hrtf-tests/MIT'
    dt = np.dtype('>i2')

    if (azim < 0) or (azim > 180):
        print('azimuth must be between 0 and 180 degrees')
    elif (elev < -40) or (elev > 90):
        print('azimuth must be between 0 and 180 degrees')
	
    if (select == 'L'):
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        larray = np.fromfile(pathname, dt, -1, "")
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        rarray = np.fromfile(pathname, dt, -1, "")
        outputarray = np.vstack((larray, rarray))
        return(outputarray)
    elif (select == 'R'):
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        larray = np.fromfile(pathname, dt, -1, "")
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        rarray = np.fromfile(pathname, dt, -1, "")
        outputarray = np.vstack((larray, rarray))
    elif (select == 'H'):
        #nothing here yet
	print("this isn't a thing yet")
    else:
        print("something went wrong")

    flipazim = 360 - azim
    if (flipazim == 360):
        flipazim = 0

    return(outputarray) 

#sets the file path to the .dat file containing the hrtf data
#setting root(and subdir??) in readraw and writeraw keeps
#the originals and modified versions separate
def hrtfpath(root, subdir, select, ext, elev, azim):
    x = '/'
    return(root+x+subdir+x+"elev"+str(elev)+x+select+str(elev)+"e"+str(azim)+"a"+ext)

#writes a modified version of the output array returned by 
#readraw to a new binary file in the modified directory
def writeraw(hrtfarray, elev, azim, select):
    subdir = "full"
    root = "/home/gilmoregrills/hrtf-tests/modified"
    writepath = hrtfpath(root, subdir, select, ".dat", elev, azim)
    hrtfarray.tofile(writepath)

#hardcoded function call for testing purposes
hrtf = readhrtf(40, 109, "L")
print(hrtf)
print(readraw("/home/gilmoregrills/hrtf-tests/modified/test.dat"))
##writeraw(hrtf, "test.dat") - either problem w/ write format or I need to split two arrays before writing
