import numpy as np

def readraw(pathname)
#again, original matlab script stolen from Bill Gardner
#and the MIT Media Lab

#should be read-only
#the matlab script is able to specify the machine format
#numpy has functions for reading binaries
    file = numpy.fromfile(pathname, float, -1, "")#float OR short I'm not sure yet
    return(file) #this returns an array of float-length numbers/binary chunks
    #so we're passing back an array? 
    funtionToCloseBinaries(file)
    
    #this is in the original file:
    #return as row vector, +/- max
    x = x' / 32768
    #this is because!! the readf function in matlab returns the float-length binary
    #chunks as elements of a single-column vector! This line of code
    #transforms the single column vector into a single ROW vector, which is
    #functionally identical to an ARRAY!!! 
    
    #I now have all I need to actually finish this file
    
