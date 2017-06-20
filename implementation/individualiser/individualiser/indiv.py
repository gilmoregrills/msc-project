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


#PCA on an input Matrix, returning PCs, PCWs, etc
def runPCA(inputMatrix):



#model PCWs as spherical harmonics
def spherHarm(weights):



#reconstruct an HRTF from PCW etc
def reconstruct(weights, components, mean):



#use fft function to transform from HRTF to HRIR
def transformData(inputData):
