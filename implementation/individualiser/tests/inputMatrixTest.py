import sys
sys.path.append('../')
import individualiser.indiv as indiv
import numpy as np

data = indiv.prepareInputMatrix('CIPIC')
inputMatrix = data[0]
allSubjects = data[1]

print inputMatrix.shape
print len(allSubjects)
print allSubjects[0]['hrir_l'].shape

if inputMatrix[0][0] == allSubjects[0]['hrir_l'][0][0][0]:
    print "test1 success!"
else:
    print "test1 failed"
if inputMatrix[0][1] == allSubjects[1]['hrir_l'][0][0][0]:
    print "test2 success!"
else: 
    print "test2 failed"
if inputMatrix[0][56249] == allSubjects[44]['hrir_l'][24][49][0]:
    print "test3 success!"
else:
    print inputMatrix[0][43]
    print allSubjects[43]['hrir_l'][0][0][0]
    print "test3 failed"

if inputMatrix[100][56249] == allSubjects[44]['hrir_l'][24][49][100]:

    print "test4 success!"
else:
    print inputMatrix[100][56249]
    print "test4 failed"

if inputMatrix.shape[0] == 101 and inputMatrix.shape[1] == 56250:
    print "test5 success!"
else:
    print "test5 failed"

