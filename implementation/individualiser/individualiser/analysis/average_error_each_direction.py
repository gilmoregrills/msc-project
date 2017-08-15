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

print output, output.shape

# plot the output array!
fig = plot.figure()
ax = plot.subplot(111)
lines = ax.plot(output.transpose())
for j in range(0, len(lines)):
	print ", ".join(map(str, utils.DIRECTIONS[j]))
	lines[j].set_label(" ".join(map(str, utils.DIRECTIONS[j])))
#lines[j].set_label(" ".join(map(str, utils.DIRECTIONS[j])))
print "number of lines", len(lines)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.15,
                 box.width, box.height * 0.9])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09),
          fancybox=True, shadow=True, ncol=5)
plot.ylabel('Total Error (degrees)')
plot.xlabel('Iterations')
plot.show()