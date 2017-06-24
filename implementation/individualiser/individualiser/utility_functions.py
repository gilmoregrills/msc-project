import os
import scipy.io as sio
import numpy as np
import sklearn.decomposition as decomp

# take a database name as input, returns an array of data
# for cipic full db, the structure is: [45, 2, 25, 50, 202/101]
def fetch_database(database, as_hrtf):
    path = ""
    if database == "CIPIC" or database == "cipic":
        path = "../databases/CIPIC/CIPIC_hrtf_database/standard_hrir_database/"

    subject_dirs = sorted(os.listdir(path))# subject directory names, chrono sorted
    subject_dirs.remove("show_data")# remove the matlab scripts folder name
    all_subjects = []

    # gather data for each subject, append to list
    for sub_dir in subject_dirs: 
        subject = sio.loadmat(path+sub_dir+"/hrir_final.mat")
        all_subjects.append(subject) 
    
    # if required, fft all data
    # MUST CHECK IF THIS IS FFT-ING CORRECTLY
    if as_hrtf == True:
        for subject in all_subjects:
            subject['hrir_l'] = np.fft.rfft(subject['hrir_l'])
            subject['hrir_r'] = np.fft.rfft(subject['hrir_r'])
    
    output_matrix = np.empty([45, 2, 25, 50, len(all_subjects[0]['hrir_l'][0][0])])
    
    for subject in range(0, len(all_subjects)):
        output_matrix[subject][0] = all_subjects[subject]['hrir_l']
        output_matrix[subject][1] = all_subjects[subject]['hrir_r']
     
    return output_matrix

# take database matrix as input, restructures it for PCA
# var all_participants is a boolean, if False produces input array of 1 subject
def restructure_data(database_matrix, all_participants):
    
    # initialise outputs
    output_matrix = []

    # now rearrange that data into the currect output_matrix structure
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
        output_matrix = np.empty([len(database_matrix[0][0])*len(database_matrix[0][0][0]), len(database_matrix[0][0][0][0])*2])
        output_sample_index = 0
        input_sample_index = 0
        for sample in range(0, len(database_matrix[0][0][0][0])):
            counter = 0
            for azimuth in range(0, len(database_matrix[0][0])):
                for elevation in range(0, len(database_matrix[0][0][0])):
                    tmp = np.empty([45]) # temporary variable for calculating the mean HRTF
                    for subject in range(0, len(database_matrix)): 
                        tmp[subject] = database_matrix[subject][0][azimuth][elevation][input_sample_index]
                    output_matrix[counter][output_sample_index] = np.mean(tmp)
                    counter += 1
            counter = 0
            output_sample_index += 1
            for azimuth in range(0, len(database_matrix[0][1])):
                for elevation in range(0, len(database_matrix[0][1][0])):
                    tmp = np.empty([45]) # temporary variable for calculating the mean HRTF
                    for subject in range(0, len(database_matrix)): 
                        tmp[subject] = database_matrix[subject][1][azimuth][elevation][input_sample_index]
                    output_matrix[counter][output_sample_index] = np.mean(tmp)
                    counter += 1
            output_sample_index += 1
            input_sample_index += 1

    # returning subject data for testing scripts
    return output_matrix

# creates PCA object and trains/fits it
def train_pca(input_matrix, components):
    pca = decomp.PCA(n_components=components)
    pca.fit(input_matrix)
    return pca

# takes a trained PCA object/model, and an input matrix, and returns the PCs/features
def pca_transform(pca_model, input_matrix):
    output_matrix = pca_model.transform(input_matrix)
    return output_matrix

# takes a trained PCA model with a previously-transformed input matrix, and returns
# a matrix matching the original input (the restructured HRTF)
def pca_reconstruct(pca_model, input_matrix):
    output_matrix = pca_model.inverse_transform(input_matrix)
    return output_matrix

# model PCWs as spherical harmonics
def spher_harm(weights):
    return


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
# if the inverse flag is true it calls the inverse fft, to go from
# hrtf to hrir!
def fourier_transform(input_data, inverse):
    print "\nStarting FFT \nInput matrix dimension is:"
    print np.ndim(input_data)
    print "\nInput matrix length is:"
    print input_data.size
 
    if inverse == False:
        return_list = ["", ""]
        return_list[1] = np.fft.rfftfreq(input_data.size, d=1./44100)# to be used to label axes?
        if np.ndim(input_data) == 1:
            print("\nperforming 1D fft\n")
            return_list[0] = np.fft.rfft(input_data)
            return return_list
        elif np.ndim(input_data) == 2:
            print("\nperforming 2D fft\n")
            return_list[0] = np.fft.rfft2(input_data) 
        else:
            print("\nperforming ND fft\n")
            return_list[0] = np.fft.rfftn(input_data)

    elif inverse == True:
        if input_data.shape == 1:
            return np.fft.ifft(input_data)
        elif input_data.shape == 2:
            return np.fft.ifft2(input_data)
        else:
            return np.fft.ifftn(input_data)
