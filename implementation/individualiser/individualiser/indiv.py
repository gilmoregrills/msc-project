import os
import scipy.io as sio
import numpy as np
import sklearn.decomposition as decomp

#take database as input, prepare correct input matrix
#should only be called when 
def prepareInputMatrix(database, asHRTF=True):
    #loop to load every subject (except KEMAR) into an array of mat objects
    #instantiate the matrix in the right dimensions/structure
    #loop again to populate the input matrix
    path = ""
    if database == "cipic" or database == "CIPIC":
        path = "../databases/CIPIC/CIPIC_hrtf_database/standard_hrir_database/"
    
    #initialise all variables
    inputMatrix = []#[(subject * direction) * samples]
    allSubjects = [] #ordered list of all subject data as matlab object thingies
    subjectDirs = sorted(os.listdir(path))
    subjectDirs.remove("show_data")
    print(subjectDirs)
    
    #gather all data for all subjects
    for subDir in subjectDirs: 
        subject = sio.loadmat(path+subDir+"/hrir_final.mat")
        print subject['name']
        allSubjects.append(subject) 
    
    #if required, fft all data
    if asHRTF == True:
        for subject in allSubjects:
            subject['hrir_l'] = np.fft.rfft(subject['hrir_l'])
            subject['hrir_r'] = np.fft.rfft(subject['hrir_r'])
    #instantiate inputMatrix array ahead of time because I'm bad at python tbh
    inputMatrix = np.empty([len(allSubjects[0]['hrir_l'][0][0]), len(allSubjects[0]['hrir_l'])*len(allSubjects[0]['hrir_l'][0])*len(allSubjects)])

    print inputMatrix.shape
    print len(allSubjects)
    print allSubjects[0]['hrir_l'].shape

    #now arrange that data into the right matrix structure!
    for sample in range(0, len(allSubjects[0]['hrir_l'][0][0])-1):
        print "currently filling bin #"
        print sample
        counter = 0
        for azimuth in range(0, len(allSubjects[0]['hrir_l'])-1):
            #print "accessing aximuth: "
            #print azimuth
            for elevation in range(0, len(allSubjects[0]['hrir_l'][0])):
                #print "accessing elevation: "
                #print elevation
                for subject in range(0, len(allSubjects)-1):
                    #print "accessing subject: "
                    #print subject['name']
                    inputMatrix[sample][counter] = allSubjects[subject]['hrir_l'][azimuth][elevation][sample]
                    counter = counter+1

    if inputMatrix[0][0] == allSubjects[0]['hrir_l'][0][0][0]:
        print "test1 success!"
    else:
        print "test1 failed"
    if inputMatrix[100][0] == allSubjects[0]['hrir_l'][0][0][100]:
        print "test2 success!"
    else: 
        print "test2 failed"
    if inputMatrix[0][56249] == allSubjects[44]['hrir_l'][24][49][0]:
        print "test3 success!"
    else:
        print "test3 failed"
    if inputMatrix[100][56249] == allSubjects[44]['hrir_l'][24][49][100]:
        print "test4 success!"
    else:
        print "test4 failed"

    print inputMatrix.shape
    return inputMatrix

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
