import numpy as np



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
    print flipazim #sanity check 
    ext = '.dat'

#the problem is happening between reading the file and the final output
#so it's either here...
    if (select == 'L'):
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        print(readraw(pathname))
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        print(readraw(pathname))
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

#OR it's here? Gotta compare to matlab scripts more
def readraw(pathname):
    file = np.fromfile(pathname, np.int16, -1, "")#matlab short is 16bit so np.int16 replaces it
    return(file) 

#this function is complete, nbd here
def hrtfpath(root, subdir, select, ext, elev, azim):
    x = '/'
    return(root+x+subdir+x+"elev"+str(elev)+x+select+str(elev)+"e"+str(azim)+"a"+ext)

#hardcoded function call for testing purposes
readhrtf(40, 109, "L")
