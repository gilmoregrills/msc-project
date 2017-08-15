# error rate for a single subject from each 
# direction, 8 lines on a chart

import utils
import sys
import numpy as np 
import scipy as scp 
import matplotlib.pyplot as plot 

# get that data
subject = sys.argv[1]
output = utils.fetch_individual_errors(subject)

# error is an angular thing, so sum those values
output = utils.sum_errors(output)

print output, output.shape

#plot the data! 8 lines of 6 points!array
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
plot.ylabel('Error (degrees)')
plot.xlabel('Iterations')
plot.show()