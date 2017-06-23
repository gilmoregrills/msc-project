import os
import scipy.io as sio
import numpy as np
import sklearn.decomposition as decomp

# take database as input, prepare correct input matrix
# var database is only 'cipic', 'ari', 'mit' etc
# var as_hrtf, False produces restructured HRIR matrix
# var all_participants is a boolean, if False produces input array of 1 subject
# var two_dimensions is also a boolean
def restructure_data(database, as_hrtf, all_participants):
    # set the database path, atm only working with CIPIC
    path = ""
    if database == "cipic" or database == "CIPIC":
        path = "../databases/CIPIC/CIPIC_hrtf_database/standard_hrir_database/"
    
    # initialise all variables
    output_matrix = []# [(subject * direction) * samples]
    all_subjects = []# list of all subject data as matlab object thingies
    subject_dirs = sorted(os.listdir(path))# subject directory names, chrono sorted
    subject_dirs.remove("show_data")# remove the matlab scripts folder name
    
    # gather data for each subject, append to list
    for sub_dir in subject_dirs: 
        subject = sio.loadmat(path+sub_dir+"/hrir_final.mat")
        all_subjects.append(subject) 
    
    # if required, fft all data
    if as_hrtf == True:
        for subject in all_subjects:
            subject['hrir_l'] = np.fft.rfft(subject['hrir_l'])
            subject['hrir_r'] = np.fft.rfft(subject['hrir_r'])

    # now rearrange that data into the currect output_matrix structure
    if all_participants == True:
        output_matrix = np.empty([len(all_subjects[0]['hrir_l'][0][0])*2, len(all_subjects[0]['hrir_l'])*len(all_subjects[0]['hrir_l'][0])*len(all_subjects)])
        output_sample_index = 0
        input_sample_index = 0
        for sample in range(0, len(all_subjects[0]['hrir_l'][0][0]*2)): 
            counter = 0
            for azimuth in range(0, len(all_subjects[0]['hrir_l'])):
                for elevation in range(0, len(all_subjects[0]['hrir_l'][0])):
                    for subject in range(0, len(all_subjects)): 
                        output_matrix[output_sample_index][counter] = all_subjects[subject]['hrir_l'][azimuth][elevation][input_sample_index]
                        # counter just provides a row index for output_matrix
                        counter += 1
            output_sample_index += 1
            counter = 0
            for azimuth in range(0, len(all_subjects[0]['hrir_l'])):
                for elevation in range(0, len(all_subjects[0]['hrir_l'][0])):
                    for subject in range(0, len(all_subjects)): 
                        output_matrix[output_sample_index][counter] = all_subjects[subject]['hrir_r'][azimuth][elevation][input_sample_index]
                        # counter just provides a row index for output_matrix
                        counter += 1
            output_sample_index += 1
            input_sample_index += 1

    # generate a 200*1250 2D array representing the mean value of one participant 
    elif all_participants == False:
        output_matrix = np.empty([len(all_subjects[0]['hrir_l'][0][0])*2, len(all_subjects[0]['hrir_l'])*len(all_subjects[0]['hrir_l'][0])])
        output_sample_index = 0
        input_sample_index = 0
        for sample in range(0, len(all_subjects[0]['hrir_l'][0][0])):
            counter = 0
            for azimuth in range(0, len(all_subjects[0]['hrir_l'])):
                for elevation in range(0, len(all_subjects[0]['hrir_l'][0])):
                    tmp = np.empty([45]) # temporary variable for calculating the mean HRTF
                    for subject in range(0, len(all_subjects)): 
                        tmp[subject] = all_subjects[subject]['hrir_l'][azimuth][elevation][input_sample_index]
                    output_matrix[output_sample_index][counter] = np.mean(tmp)
                    counter += 1
            counter = 0
            output_sample_index += 1
            for azimuth in range(0, len(all_subjects[0]['hrir_l'])):
                for elevation in range(0, len(all_subjects[0]['hrir_l'][0])):
                    tmp = np.empty([45]) # temporary variable for calculating the mean HRTF
                    for subject in range(0, len(all_subjects)): 
                        tmp[subject] = all_subjects[subject]['hrir_r'][azimuth][elevation][input_sample_index]
                    output_matrix[output_sample_index][counter] = np.mean(tmp)
                    counter += 1
            output_sample_index += 1
            input_sample_index += 1

    # returning subject data for testing scripts
    return_list = [output_matrix, all_subjects]
    return return_list

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
def reconstruct(weights, components, mean):
    return


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
