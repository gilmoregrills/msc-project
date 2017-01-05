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
    root = 'gilmoregrills/hrtf-tests/MIT'
#checks that the args passed at run are a-okay
    if ((azim < 0) || (azim > 180))
        print('azimuth must be between 0 and 180 degrees')
    else if ((elev < -40) || (elev > 90))
        print('azimuth must be between 0 and 180 degrees')

#formats the filename
    flipazim = 360 - azim
    if (flipazim == 360
        flipazim = 0
    
    ext = '.dat'

    if (select == 'L')
        pathname = hrtfpath(root,'full',select,ext,elev,azim);
#pathname has been set, so I think we print readraw which is 
#another script, passing pathname to THAT
        print(readraw(pathname))
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        print(readraw(pathname))
    else if (select == 'R')
        pathname = hrtfpath(root,'full',select,ext,elev,flipazim)
        print(readraw(pathname))
        pathname = hrtfpath(root,'full',select,ext,elev,azim)
        print(readraw(pathname))      
    else if (select == 'H')
        pathname = hrtfpath(root,'compact',select,ext,elev,azim)
        tmp = readraw(pathname);
        print("this one actually doesn't work")
    else
        print("something went wrong")


