# fetch error for each direction, find
# the average error rates for each plot
# as eight lines!
import utils
import sys
import numpy as np 
import scipy as scp 
import matplotlib.pyplot as plot 
import os

subjects = len(os.listdir("subjects"))

output = np.zeros([8, 6])
output.flags.writeable = True

for i in range(0, 8):
	tmp = utils.fetch_all_for_direction(i)
	tmp = utils.sum_errors(tmp)
	output[i] = utils.column_mean(tmp)

print output

# plot the output array!
lines = plot.plot(output)
for j in range(0, len(lines)):
	print ", ".join(map(str, utils.DIRECTIONS[j]))
	lines[j].label = " ".join(map(str, utils.DIRECTIONS[j]))
#lines[j].set_label(" ".join(map(str, utils.DIRECTIONS[j])))
print "number of lines", len(lines)
plot.legend(loc="best")
plot.ylabel('Total Error (degrees)')
plot.xlabel('Iterations')
plot.show()