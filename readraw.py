def readraw(pathname)
#again, original matlab script stolen from Bill Gardner
#and the MIT Media Lab

#should be read-only
#the matlab script is able to specify the machine format
#numpy has functions for reading binaries
    file = functionToOpenBinaries(pathname, specify IEEE float w/ big-endian ordering)
    if (file == "")
        print("error message")
    functionToReadBinaries(file, size=infinity(numpy?), precision=short)

    funtionToCloseBinaries(file)

    #return as row vetor, +/- max
    #from matlab it ends with:
    x = x' / 32768
    #so in python it's 
    return(x / 32768) 
    #i think in the original it's doing like:
    #return(functionToReadBinaries etc)
    #return(return / 32768) 
    #or
    #x = fucntionToReadBinaries
    #return(x / 32768)
    #what happens if I just return the read of the binary
