import numpy as np
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
    
#home directory/path to the folder where 'full' is kept
    root = '/home/gilmoregrills/hrtf-tests/MIT'
    print root
#checks that the args passed at run are a-okay
    if (azim < 0) or (azim > 180):
        print('azimuth must be between 0 and 180 degrees')
    elif (elev < -40) or (elev > 90):
        print('azimuth must be between 0 and 180 degrees')

#formats the filename
    flipazim = 360 - azim
    if (flipazim == 360):
        flipazim = 0
     
    ext = '.dat'

#decides what file to access/what information to pull depending
#on the L/R parameters passed, then stores the information in
#a 2:512 array and prints the array
    if (select == 'L'):
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        larray = readraw(pathname)
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        rarray = readraw(pathname)
        outputarray = np.vstack((larray, rarray))
        print(outputarray)
    elif (select == 'R'):
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        print(readraw(pathname))
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        print(readraw(pathname))      
    elif (select == 'H'):
        pathname = hrtfpath(root,'compact',select,ext,elev,azim)
        tmp = readraw(pathname);
        print("this one actually doesn't work")
    else:
        print("something went wrong")

#sets datatype to big-endian-16-bit-integer
#then accesses the file based on the output
#of pathname, returns array of 512 indexes
dt = np.dtype('>i2')
def readraw(pathname):
    file = np.fromfile(pathname, dt, -1, "")
    #file = np.divide(file, 32768) matlab script has similar line
    #to this one, but it seemed to give insanely small decimals
    #not the integers described in hrtfdoc.txt
    return(file) 

#sets the file path to the .dat file containing the hrtf data
def hrtfpath(root, subdir, select, ext, elev, azim):
    x = '/'
    return(root+x+subdir+x+"elev"+str(elev)+x+select+str(elev)+"e"+str(azim)+"a"+ext)

#hardcoded function call for testing purposes
readhrtf(40, 109, "L")
