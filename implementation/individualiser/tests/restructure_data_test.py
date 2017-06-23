import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np

print "\nTesting all_participants = True and two_dimensions = True\n"

data = util.restructure_data('CIPIC', True, True)
input_matrix = data[0]
all_subjects = data[1]

print "Returned matrix shape:"
print input_matrix.shape
print "Number of participants:"
print len(all_subjects)

if input_matrix[0][0] == all_subjects[0]['hrir_l'][0][0][0]:
    print "test1 success!"
else:
    print "test1 failed"
    print input_matrix[0][0]
    print all_subjects[0]['hrir_l'][0][0][0]
     
if input_matrix[0][1] == all_subjects[0]['hrir_r'][0][0][0]:
    print "test2 success!"
else: 
    print "test2 failed"
    print input_matrix[0][1] 
    print all_subjects[1]['hrir_l'][0][0][0]

if input_matrix[56249][0] == all_subjects[44]['hrir_l'][24][49][0]:
    print "test3 success!"
else:
    print input_matrix[0][43]
    print all_subjects[43]['hrir_l'][0][0][0]
    print "test3 failed"

if input_matrix[56249][201] == all_subjects[44]['hrir_r'][24][49][100]:

    print "test4 success!"
else:
    print "test4 failed"
    print input_matrix[100][56249]
    print all_subjects[44]['hrir_l'][24][49][100]

if input_matrix.shape[0] == 56250 and input_matrix.shape[1] == 202:
    print "test5 success!"
else:
    print "test5 failed"
    print input_matrix.shape[0]
    print input_matrix.shape[1]

print "\nAttempting to re-form HRTF set"
reassembled_set = util.restructure_to_hrtf(input_matrix, True)
print "\nFull HRTF set reassembled to SUBJECTxLRxAZIMUTHxELEVATION matrix"
print reassembled_set.shape

print "\nTesting all_participants = False and two_dimensions = True\n"

data3 = util.restructure_data('CIPIC', True, False)
input_matrix = data3[0]
all_subjects = data3[1]
test_array1 = np.empty([45])
test_array2 = np.empty([45])
for subject in range(0, len(all_subjects)):
    test_array1[subject] = all_subjects[subject]['hrir_l'][0][0][0]
for subject in range(0, len(all_subjects)):
    test_array2[subject] = all_subjects[subject]['hrir_r'][0][0][0]

test_mean2 = np.mean(test_array2)
test_mean1 = np.mean(test_array1)

print "Returned matrix shape:"
print input_matrix.shape
print "Number of participants:"
print len(all_subjects)

if input_matrix[0][0] == test_mean1:
    print "test1 success!"
else:
    print input_matrix[0][0]
    print test_mean2
    print "test1 failed"

if input_matrix[0][1] == test_mean2:
    print "test2 success!"
else:
    print input_matrix[0][0]
    print test_mean2
    print "test2 failed"

print "\nAttempting to re-form single HRTF"
reassembled_matrix = util.restructure_to_hrtf(input_matrix, False)
print "\nSingle HRTF matrix reassembled to L/R hrtfs"
print reassembled_matrix.shape

if test_mean1 == reassembled_matrix[0][0][0][0]:
    print "test1 success!"
else:
    print "test1 failed"
if test_mean2 == reassembled_matrix[1][0][0][0]:
    print "test2 success!"
else: 
    print "test2 failed"
