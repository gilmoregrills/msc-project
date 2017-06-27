import sys
sys.path.append('../')
import lmdb_data.lmdb_interface as lmdb
import numpy as np

print "\nGenerating Data"
ex1 = np.zeros([45, 2, 25, 50, 200])
ex2 = np.zeros([2, 25, 50, 200])
ex3 = np.zeros([56250, 400])
ex4 = np.zeros([1250, 200])

print "\nStoring Data"
print "1"
s1 = lmdb.store('ex1', ex1)
print "2"
s2 = lmdb.store('ex2', ex2)
print "3"
s3 = lmdb.store('ex3', ex3)
print "4"
s4 = lmdb.store('ex4', ex4)

if s1 == True and s2 == True and s3 == True and s4 == True:
    print "store test passed"
else:
    print "store test failed"

print "\nFetching Data"
print "1"
f1 = lmdb.fetch('ex1')
print "2"
f2 = lmdb.fetch('ex2')
print "3"
f3 = lmdb.fetch('ex3')
print "4"
f4 = lmdb.fetch('ex4')

print f1.size
print f2.size
print f3.size
print f4.size

print "\nDeleting Data"
print "1"
d1 = lmdb.delete('ex1')
print d1
print "2"
d2 = lmdb.delete('ex2')
print d2
print "3"
d3 = lmdb.delete('ex3')
print d3
print "4"
d4 = lmdb.delete('ex4')
print d4

if d1 == True and d2 == True and d3 == True and d4 == True:
    print "delete test passed"
else: 
    print "delete test failed"
