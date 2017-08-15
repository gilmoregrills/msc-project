# fetch all error rates for a single direction
# and plot them on an appropriate chart??

import utils
import sys
import numpy as np 
import os
import scipy as scp 
import matplotlib.pyplot as plot 
import simplejson as json

direction = int(sys.argv[1]) - 1# int, 1-8

subjects = len(os.listdir("subjects"))

output = []

for subject in range(1, subjects+1):
	print "fetching data from subject: ", subject
	path = "subjects/"+ str(subject) + ".json"
	file = open(path, "r")
	data = json.loads(file.read())["data"]
	# now data from the subject is loaded into data
	direction_data = []
	for entry in data:
		directo = entry['src_loc']
		index = utils.DIRECTIONS.index(directo)
		if index == direction:
			direction_data.append(entry)
	# now direction_data is a 6 index array 
	for i in  range(0, len(direction_data)-1):
		output.append({
			"angle1": direction_data[i]['prcv_loc'],
			"angle2": direction_data[i+1]['prcv_loc'],
			"pcws1": direction_data[i]['pcws_before'],
			"pcws2": direction_data[i+1]['pcws_before'],
			"change": direction_data[i]['direction']
			})
		print i

print len(output)
print output[len(output)-1]

