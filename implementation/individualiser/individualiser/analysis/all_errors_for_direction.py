# fetch all error rates for a single direction
# and plot them on an appropriate chart??

import utils
import sys
import numpy as np 
import scipy as scp 
import matplotlib.pyplot as plot 

direction = int(sys.argv[1]) - 1# int, 1-8

errors = utils.fetch_all_for_direction(direction)
print errors.shape

errors = utils.sum_errors(errors)
print errors.shape 

# now plot those onto something in matplotlib?