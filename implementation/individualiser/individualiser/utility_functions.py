import os
import scipy.io as sio
import numpy as np
import sklearn.decomposition as decomp
import pca_functions as pca


# take a database name as input, returns an array of data
# for cipic full db, the structure is: [45, 2, 25, 50, 202/101]
def fetch_database(database):
    path = ""
    if database == "CIPIC" or database == "cipic":
        path = "../hrtf_data/CIPIC/CIPIC_hrtf_database/standard_hrir_database/"

    subject_dirs = sorted(os.listdir(path))# subject directory names, chrono sorted
    subject_dirs.remove("show_data")# remove the matlab scripts folder name
    all_subjects = []

    # gather data for each subject, append to list
    for sub_dir in subject_dirs: 
        subject = sio.loadmat(path+sub_dir+"/hrir_final.mat")
        all_subjects.append(subject) 
    
    output_matrix = np.empty([45, 2, 25, 50, len(all_subjects[0]['hrir_l'][0][0])])
    
    for subject in range(0, len(all_subjects)):
        output_matrix[subject][0] = all_subjects[subject]['hrir_l']
        output_matrix[subject][1] = all_subjects[subject]['hrir_r']
     
    return output_matrix

# takes as input a [45, 2, 25, 50, n] array
# returns a [2, 25, 50, n] array
def average_hrtf(database):
    output_matrix = np.empty([2, len(database[0][0]), len(database[0][0][0]), len(database[0][0][0][0])])
    sample_counter = 0
    for sample in range(0, len(database[0][0][0][0])): 
        for azimuth in range(0, len(database[0][0])):
            for elevation in range(0, len(database[0][0][0])):
                tmp_l = np.empty([len(database)])
                tmp_r = np.empty([len(database)])
                for subject in range(0, len(database)):
                    tmp_l[subject] = database[subject][0][azimuth][elevation][sample]
                    tmp_r[subject] = database[subject][1][azimuth][elevation][sample]
                output_matrix[0][azimuth][elevation][sample] = np.mean(tmp_l)
                output_matrix[1][azimuth][elevation][sample] = np.mean(tmp_r)
    
    return output_matrix




# take database matrix as input, restructures it for PCA
# var all_participants is a boolean, if False produces input array of 1 subject
def restructure_data(database_matrix, all_participants): 
    # initialise outputs
    output_matrix = []

    if all_participants == True:
        output_matrix = np.empty([len(database_matrix[0][0])*len(database_matrix[0][0][0])*len(database_matrix), len(database_matrix[0][0][0][0])*2])
        output_sample_index = 0
        input_sample_index = 0
        for sample in range(0, len(database_matrix[0][0][0][0]*2)): 
            counter = 0
            for azimuth in range(0, len(database_matrix[0][0])):
                for elevation in range(0, len(database_matrix[0][0][0])):
                    for subject in range(0, len(database_matrix)): 
                        output_matrix[counter][output_sample_index] = database_matrix[subject][0][azimuth][elevation][input_sample_index]
                        # counter just provides a row index for output_matrix
                        counter += 1
            output_sample_index += 1
            counter = 0
            for azimuth in range(0, len(database_matrix[0][1])):
                for elevation in range(0, len(database_matrix[0][1][0])):
                    for subject in range(0, len(database_matrix)): 
                        output_matrix[counter][output_sample_index] = database_matrix[subject][1][azimuth][elevation][input_sample_index]
                        # counter just provides a row index for output_matrix
                        counter += 1
            output_sample_index += 1
            input_sample_index += 1

    # generate a 200*1250 2D array representing the mean value of one participant 
    elif all_participants == False:
        output_matrix = np.empty([len(database_matrix[0])*len(database_matrix[0][0]), len(database_matrix[0][0][0])*2])
        output_sample_index = 0
        input_sample_index = 0
        counter = 0
        for sample in range(0, len(database_matrix[0][0][0])):
            for azimuth in range(0, len(database_matrix[0])):
                for elevation in range(0, len(database_matrix[0][0])):
                    output_matrix[counter][output_sample_index] = database_matrix[0][azimuth][elevation][sample]
                    counter += 1
            counter = 0
            output_sample_index += 1
            for azimuth in range(0, len(database_matrix[1])):
                for elevation in range(0, len(database_matrix[1][0])):
                    output_matrix[counter][output_sample_index] = database_matrix[1][azimuth][elevation][sample]
                    counter += 1
            counter = 0
            output_sample_index += 1
            input_sample_index += 1

    # returning subject data for testing scripts
    return output_matrix

# reconstruct an HRTF from PCW etc
def restructure_inverse(input_matrix, all_subjects):
    # First let's split input into L and R arrays
    input_l = np.empty([len(input_matrix), len(input_matrix[0])/2])
    input_r = np.empty([len(input_matrix), len(input_matrix[0])/2])
    for n in range(0, len(input_l)):
        counter = 0
        for m in range(0, len(input_l[0])):
            input_l[n][m] = input_matrix[n][counter]
            counter += 1
            input_r[n][m] = input_matrix[n][counter]
            counter += 1
    #print "\nCurrent Matrices:"
    #print input_l.shape
    #print input_r.shape
     
    # if working with a single HRTF
    if all_subjects == False:
        hrtf_l = np.empty([25, 50, 101])
        hrtf_r = np.empty([25, 50, 101])
        counter2 = 0
        for x in range(0, 25):
            for y in range(0, 50):
                hrtf_l[x][y] = input_l[counter2]
                hrtf_r[x][y] = input_r[counter2]
                counter2 += 1
        output = np.array([hrtf_l, hrtf_r])

    # else if working with the full DB
    elif all_subjects == True:
        hrtf_set = np.empty([45, 2, 25, 50, 101])
        counter3 = 0
        for x in range(0, 25):
            for y in range(0, 50):
                for z in range(0, 45):
                    hrtf_set[z][0][x][y] = input_l[counter3]
                    hrtf_set[z][1][x][y] = input_r[counter3]
                    counter3 += 1
        print counter3
        output = hrtf_set

    return output


# uses the numpy.fft set of functions to transform input matrices 
# if the inverse flag is true it calls the inverse fft
# specify whether it's full dataset of single set, there's 
# a one-loop difference between processes
def fourier_transform(input_data, inverse, all_subjects):
    print "\nStarting FFT \nInput matrix dimension is:"
    print np.ndim(input_data)
    print "\nInput matrix is:"
    print input_data.shape
    return_list = "" 
    if inverse == False:
        return_list = ["", ""]
        return_list[1] = np.fft.rfftfreq(input_data.size, d=1./44100)# to be used to label axes
        if all_subjects == True:
            return_list[0] = np.empty([45, 2, 25, 50, 101])
            for subject in range(0, 45):
                for azimuth in range(0, 25):
                    for elevation in range(0, 50):
                        return_list[0][subject][0][azimuth][elevation] = np.fft.rfft(input_data[subject][0][azimuth][elevation])
                        return_list[0][subject][1][azimuth][elevation] = np.fft.rfft(input_data[subject][1][azimuth][elevation])
        if all_subjects == False:
            return_list[0] = np.empty([2, 25, 50, 101])    
            for azimuth in range(0, 25):
                for elevation in range(0, 50):
                    return_list[0][0][azimuth][elevation] = np.fft.rfft(input_data[0][azimuth][elevation])
                    return_list[0][1][azimuth][elevation] = np.fft.rfft(input_data[1][azimuth][elevation])

    elif inverse == True: 
        if all_subjects == True:
            return_list = np.empty([45, 2, 25, 50, 200])
            for subject in range(0, 45):
                for azimuth in range(0, 25):
                    for elevation in range(0, 50):
                        return_list[subject][0][azimuth][elevation] = np.fft.irfft(input_data[subject][0][azimuth][elevation])
                        return_list[subject][1][azimuth][elevation] = np.fft.irfft(input_data[subject][1][azimuth][elevation])
        if all_subjects == False:
            return_list = np.empty([2, 25, 50, 200])    
            for azimuth in range(0, 25):
                for elevation in range(0, 50):
                    return_list[0][azimuth][elevation] = np.fft.irfft(input_data[0][azimuth][elevation])
                    return_list[1][azimuth][elevation] = np.fft.irfft(input_data[1][azimuth][elevation])
            
    return return_list
