import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np

print "\nFetching database data as 5D array"
hrir_database = util.fetch_database('cipic')

print "\nDatabase fetched, shape: "
print hrir_database.shape

database = np.empty([45, 2, 25, 50, 101])

print "\nTransforming database to hrtf\n"
data = util.fourier_transform(hrir_database, False, True)
database = data[0]

print "New shape:"
print database.shape

print "\nTesting all_participants = True and two_dimensions = True\n"

input_matrix = util.restructure_data(database, True)

print "Returned matrix shape:"
print input_matrix.shape
print "Number of participants:"
print len(database)

if input_matrix[0][0] == database[0][0][0][0][0]:
    print "test1 success!"
else:
    print "test1 failed"
    print input_matrix[0][0]
    print database[0][0][0][0][0]
     
if input_matrix[0][1] == database[0][1][0][0][0]:
    print "test2 success!"
else: 
    print "test2 failed"
    print input_matrix[0][1] 
    print database[1][0][0][0][0]

if input_matrix[56249][0] == database[44][0][24][49][0]:
    print "test3 success!"
else:
    print input_matrix[0][43]
    print database[43][0][0][0][0]
    print "test3 failed"

if input_matrix[56249][201] == database[44][1][24][49][100]:

    print "test4 success!"
else:
    print "test4 failed"
    print input_matrix[100][56249]
    print database[44][0][24][49][100]

if input_matrix.shape[0] == 56250 and input_matrix.shape[1] == 202:
    print "test5 success!"
else:
    print "test5 failed"
    print input_matrix.shape[0]
    print input_matrix.shape[1]

print "\nAttempting to re-form HRTF set"
reassembled_set = util.restructure_inverse(input_matrix, True)
print "\nFull HRTF set reassembled to SUBJECTxLRxAZIMUTHxELEVATION matrix"
print reassembled_set.shape


print "\nTesting single average HRTF\n"

average_hrtf = util.average_hrtf(database)

input_matrix = util.restructure_data(average_hrtf, False)
test_array1 = np.empty([45])
test_array2 = np.empty([45])
for subject in range(0, len(database)):
    test_array1[subject] = database[subject][0][0][0][0]
for subject in range(0, len(database)):
    test_array2[subject] = database[subject][1][0][0][0]

test_mean2 = np.mean(test_array2)
test_mean1 = np.mean(test_array1)

print "Returned matrix shape:"
print input_matrix.shape

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
reassembled_matrix = util.restructure_inverse(input_matrix, False)
print "\nSingle HRTF matrix reassembled to L/R hrtfs"
print reassembled_matrix.shape

if average_hrtf[0][0][0][0] == reassembled_matrix[0][0][0][0]:
    print "test1 success!"
else:
    print "test failed"


