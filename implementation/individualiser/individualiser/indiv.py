import os.path
import scipy.io as sio
import numpy as np
import sklearn.decomposition as decomp

#take database as input, prepare correct input matrix
#should only be called when 
def prepareInputMatrix(databasePath):
    #loop to load every subject (except KEMAR) into an array of mat objects
    #instantiate the matrix in the right dimensions/structure
    #loop again to populate the input matrix
    return

#PCA on an input Matrix, returning PCs, PCWs, etc
def runPCA(inputMatrix):
    return


#model PCWs as spherical harmonics
def spherHarm(weights):
    return


#reconstruct an HRTF from PCW etc
def reconstruct(weights, components, mean):
    return


#uses the numpy.fft set of functions to transform input matrices 
#if the inverse flag is true it calls the inverse fft, to go from
#hrtf to hrir!
def fourierTransform(inputData, inverse):
    print "\nStarting FFT \nInput matrix dimension is:"
    print np.ndim(inputData)

    if inverse == False:
        returnList = list()
        returnList[1] = np.fft.fftfreq(inputData.len)#this bit should help as per stackexchange
        if np.ndim(inputData) == 1:
            print("\nperforming 1D fft\n")
            returnList[0] = np.fft.fft(inputData)
            return returnList
        elif np.ndim(inputData) == 2:
            print("\nperforming 2D fft\n")
            returnList[0] = np.fft.fft2(inputData)
        else:
            print("\nperforming ND fft\n")
            returnList[0] = np.fft.fftn(inputData)

    elif inverse == True:
        if inputData.shape == 1:
            return np.fft.ifft(inputData)
        elif inputData.shape == 2:
            return np.fft.ifft2(inputData)
        else:
            return np.fft.ifftn(inputData)
