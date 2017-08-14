# error rate for a single subject from each 
# direction, 8 lines on a chart

import utils
import sys
import numpy as np 
import scipy as scp 
import matplotlib.pyplot as plot 

# get that data
subject = sys.argv[1]
errors = utils.fetch_individual_errors(subject)

# error is an angular thing, so sum those values
errors = utils.sum_errors(errors)

print errors, errors.shape

#plot the data! 8 lines of 6 points!array