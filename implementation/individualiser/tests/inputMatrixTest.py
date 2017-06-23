import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np


print "\nTesting all_participants = True and two_dimensions = True\n"

data = util.restructure_data('CIPIC', True, True, True)
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
if input_matrix[0][1] == all_subjects[1]['hrir_l'][0][0][0]:
    print "test2 success!"
else: 
    print "test2 failed"
if input_matrix[0][56249] == all_subjects[44]['hrir_l'][24][49][0]:
    print "test3 success!"
else:
    print input_matrix[0][43]
    print all_subjects[43]['hrir_l'][0][0][0]
    print "test3 failed"

if input_matrix[100][56249] == all_subjects[44]['hrir_l'][24][49][100]:

    print "test4 success!"
else:
    print input_matrix[100][56249]
    print "test4 failed"

if input_matrix.shape[0] == 101 and input_matrix.shape[1] == 56250:
    print "test5 success!"
else:
    print "test5 failed"

print "\nTesting all_participants = True and two_dimensions = False\n"

data2 = util.restructure_data('CIPIC', True, True, False)
input_matrix = data2[0]
all_subjects = data2[1]

print "Returned matrix shape:"
print input_matrix.shape
print "Number of participants:"
print len(all_subjects)

if input_matrix[0][0][0] == all_subjects[0]['hrir_l'][0][0][0]:
    print "test1 success!"
else:
    print "test1 failed"
if input_matrix[0][1][0] == all_subjects[0]['hrir_l'][0][1][0]:
    print "test2 success!"
else:
    print "test2 failed"
if input_matrix[100][1249][44] == all_subjects[44]['hrir_l'][24][49][100]:
    print "test3 success!"
else:
    print "test3 failed"
if input_matrix.shape[0] == 101 and input_matrix.shape[1] == 1250:
    print "test4 success!"
else:
    print "test4 failed"

print "\nTesting all_participants = False and two_dimensions = True\n"

data3 = util.restructure_data('CIPIC', True, False, True)
input_matrix = data3[0]
all_subjects = data3[1]

print "Returned matrix shape:"
print input_matrix.shape
print "Number of participants:"
print len(all_subjects)

if input_matrix[0][0] == np.mean(data3[0][0][0]):
    print "test1 success!"
else:
    print input_matrix[0][0]
    print np.mean(data3[0][0][0])
    print "test1 failed"
