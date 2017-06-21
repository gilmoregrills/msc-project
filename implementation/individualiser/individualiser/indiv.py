import os
import scipy.io as sio
import numpy as np
import sklearn.decomposition as decomp

#take database as input, prepare correct input matrix
#should only be called when 
def prepareInputMatrix(databasePath, asHRTF):
    #loop to load every subject (except KEMAR) into an array of mat objects
    #instantiate the matrix in the right dimensions/structure
    #loop again to populate the input matrix
    inputMatrix = [] #[(subject * direction) * samples]
    allSubjects = []
    counter = 0
    for root, dirs, files in os.walk("../databases/CIPIC/CIPIC_hrtf_database/standard_hrir_database/")
        

    if asHRTF == True:
        return#fft on all HRIRs :|
       #inputMatrix[counter] = sio.loadmat(folder+"/hrir_final.mat") 
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
    print "\nInput matrix length is:"
    print inputData.size
 
    if inverse == False:
        returnList = ["", ""]
        returnList[1] = np.fft.rfftfreq(inputData.size, d=1./44100)#to be used to label axes?
        if np.ndim(inputData) == 1:
            print("\nperforming 1D fft\n")
            returnList[0] = np.fft.rfft(inputData)
            return returnList
        elif np.ndim(inputData) == 2:
            print("\nperforming 2D fft\n")
            returnList[0] = np.fft.rfft2(inputData) 
        else:
            print("\nperforming ND fft\n")
            returnList[0] = np.fft.rfftn(inputData)

    elif inverse == True:
        if inputData.shape == 1:
            return np.fft.ifft(inputData)
        elif inputData.shape == 2:
            return np.fft.ifft2(inputData)
        else:
            return np.fft.ifftn(inputData)
