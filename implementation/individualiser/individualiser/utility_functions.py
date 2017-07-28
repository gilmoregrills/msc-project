import os
import scipy.io as sio
import numpy as np
import sklearn.decomposition as decomp
import pca_functions as pca

CIPIC_DIRECTIONS = {
    'ELEVATION': np.linspace(-45.0, 230.625, 50),
    'AZIMUTH': np.array([-80, -65, -55, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 65, 80])
}


# take a database name as input, returns an array of data
# for cipic full db, the structure is: [45, 2, 25, 50, 202/101]
def fetch_database(path):
    if path == "CIPIC" or path == "cipic":
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


def parse_vector(vector_string):
    #input vector should be a string, parse it!
    #print type(vector_string)
    vector_string = vector_string.replace(")(", ",")
    vector_string = vector_string.replace("(", "")
    vector_string = vector_string.replace(")", "")
    vector_string = vector_string.replace(" ", "")
    vector_string = vector_string.split(",")
    print vector_string, type(vector_string), len(vector_string)
    vector_string = np.array(map(float, vector_string))
    print vector_string, type(vector_string), vector_string.size
    sound_src = np.array(vector_string[:3])
    percv_src = np.array(vector_string[3:6])
    new_src = np.array(vector_string[6:])

    #print sound_src, percv_src
    return np.array([sound_src, percv_src, new_src])


def find_angles(input_vectors):
    # split up the input array of vectors
    sound_src = input_vectors[0]
    percv_src = input_vectors[1]
    new_src = input_vectors[2]
    #print sound_src, percv_src
    # turn those vectors into angles
    sound_src_angles = np.array([np.degrees(np.arctan(sound_src[0] / sound_src[2])),
                                np.degrees(np.arctan(sound_src[1] / sound_src[2]))])
    sound_src_angles.flags.writeable = True
    percv_src_angles = np.array([np.degrees(np.arctan(percv_src[0] / percv_src[2])), 
                                np.degrees(np.arctan(percv_src[1] / percv_src[2]))])
    sound_src_angles.flags.writeable = True

    new_src_angles = np.array([np.degrees(np.arctan(new_src[0] / new_src[2])),
                                np.degrees(np.arctan(new_src[1] / new_src[2]))])
    new_src_angles.flags.writeable = True

    # turn those angles into CIPIC-esque 
    # angles, 0,0 for ahead, +/- 180 behind
    # elevation from -45 to +270
    if sound_src[2] < 0:
        sound_src_angles.put(1, sound_src_angles[1] + 180)
    if percv_src[2] < 0:
        percv_src_angles.put(1, percv_src_angles[1] + 180)
    if new_src[2] < 0:
        new_src_angles.put(1, percv_src_angles[1] + 180)

    #return array of both angles, ready for index finder
    return np.array([sound_src_angles, percv_src_angles, new_src_angles])

def cipic_indexes(angles):
    # angles is a 2*2 array of the angles of source and
    # perceived in the correct form for the coords]
    output = np.array([[0, 0], [0, 0], [0, 0]])
    for pair in range(0, 3):
        output[pair][0] = (np.abs(CIPIC_DIRECTIONS['AZIMUTH']-angles[pair][0])).argmin()
        #print "input angle: ", angles[pair][0]
        #print "output index: ", output[pair][0]
        #print "angle rounded to: ", CIPIC_DIRECTIONS['AZIMUTH'][output[pair][0]]
        output[pair][1] = (np.abs(CIPIC_DIRECTIONS['ELEVATION']-angles[pair][1])).argmin()
        #print "input angle: ", angles[pair][1]
        #print "output index: ", output[pair][1]
        #print "angle rounded to: ", CIPIC_DIRECTIONS['ELEVATION'][output[pair][1]]

    # returns a 2*2 array of indexes for the CIPIC database when structured [25][50][200]
    # output[0] is the source position index
    # output[1] is the cursor position index
    return output
    
def pcw_indexes(indexes):
    print "indexes ", indexes
    # indexes should be a 1*2 list ft azi and elev
    # output[0][0] should be primary direction
    # output[1] should be the other 8 secondary directions
    output_list = np.array([[0], [0, 0, 0, 0, 0, 0, 0, 0]])
    output_list.flags.writeable = True
    # primary direction
    output_list[0][0] = (indexes[0]*50)+indexes[1]
    # secondary directions in a square around the primary
    output_list[1][0] = (indexes[0]*50)+(indexes[1]+1)# up
    output_list[1][1] = (indexes[0]*50)+(indexes[1]-1)# down
    output_list[1][2] = ((indexes[0]-1)*50)+indexes[1]# left
    output_list[1][3] = ((indexes[0]+1)*50)+indexes[1]# right
    output_list[1][4] = ((indexes[0]-1)*50)+(indexes[1]+1)# up/left
    output_list[1][5] = ((indexes[0]+1)*50)+(indexes[1]+1)# up/right
    output_list[1][6] = ((indexes[0]-1)*50)+(indexes[1]-1)# down/left
    output_list[1][7] = ((indexes[0]+1)*50)+(indexes[1]-1)# down/right
    
    return output_list

def column_mean(pca_matrix):
    # input must be of pca input form
    # 1250*101/202/etc
    print "pca matrix size ", pca_matrix.shape[0]
    output = np.zeros(pca_matrix.shape[0])
    for column in range(0, pca_matrix.shape[0]):
        output[column] = np.mean(pca_matrix[column])
    output = output[:, np.newaxis]
    return output

def adjust_matrix(pcw_indexes, pc_matrix, directions, value):
    # directions is a 10-index list of booleans
    # pcw_indexes is an array of all the indexes that will be adjusted
    # value is the adjustment value (amount)
    pc_matrix.flags.writeable = True
    before = np.zeros([9, 10])
    after = np.zeros([9, 10])
    print "pc input matrix ", pc_matrix.shape
    # for direction in directions
    counter = 0
    print "pcw indexes ", pcw_indexes
    print "change directions: ", directions, len(directions)
    for direction in range (0, 10):# that's the change direction for each PC 
        print "counter is at :", counter
        before[0][counter] = pc_matrix[pcw_indexes[0][0]][counter]
        print "change direction for this PC: ", directions[direction]
        if directions[direction] is True:
            print "changed ", pc_matrix[pcw_indexes[0][0]][counter]
            pc_matrix[pcw_indexes[0][0]][counter] += value
            print "to ", pc_matrix[pcw_indexes[0][0]][counter]
            after[0][counter] = pc_matrix[pcw_indexes[0][0]][counter]
            for index in range (0, 8):
                before[index+1][counter] = pc_matrix[pcw_indexes[1][index]][counter]
                print "changed ", pc_matrix[pcw_indexes[1][index]][counter]
                pc_matrix[pcw_indexes[1][index]][counter] += (value/2)
                print "to ", pc_matrix[pcw_indexes[1][index]][counter]
                after[index+1][counter] = pc_matrix[pcw_indexes[1][index]][counter]
        if directions[direction] is False:
            pc_matrix[pcw_indexes[0][0]][counter] -= value
            after[0][counter] = pc_matrix[pcw_indexes[0][0]][counter]
            for index in range (0, 8):
                before[index+1][counter] = pc_matrix[pcw_indexes[1][index]][counter]
                pc_matrix[pcw_indexes[1][index]][counter] -= (value/2)
                after[index+1][counter] = pc_matrix[pcw_indexes[1][index]][counter]
        counter += 1

#        if direction is True:
#           before[0] = pc_matrix[pcw_indexes[0][0]]
#           pc_matrix[pcw_indexes[0][0]] += value
#           after[0] = pc_matrix[pcw_indexes[0][0]]
#           for index in range(0, 8):
#               before[index] = pc_matrix[index]
#               pc_matrix[index] += (value / 2)
#               after[index] = pc_matrix[index]
#       else:
#           before[0] = pc_matrix[pcw_indexes[0][0]]
#           pc_matrix[pcw_indexes[0][0]] -= value
#           after[0] = pc_matrix[pcw_indexes[0][0]]
#           for index in range(0, 8):
#               before[index] = pc_matrix[index]
#               pc_matrix[index] -= (value / 2)
#               after[index] = pc_matrix[index]
    print "before : ", before
    print "after : ", after
    return [pc_matrix, before, after]
