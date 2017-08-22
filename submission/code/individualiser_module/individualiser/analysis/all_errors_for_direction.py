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
pair = int(sys.argv[2])

subjects = len(os.listdir("subjects"))

output = []
for sublist in range(0, subjects):
	output.append([])

for subject in range(1, subjects+1):
	path = "subjects/"+ str(subject) + ".json"
	file = open(path, "r")
	data = json.loads(file.read())["data"]
	# now data from the subject is loaded into data
	direction_data = []
	for entry in data:
		directo = entry["src_loc"]
		index = utils.DIRECTIONS.index(directo)
		if index == direction:
			direction_data.append(entry)
	# now direction_data is a 6 index array 
	for i in  range(0, len(direction_data)-1):
		output[subject-1].append({
			"angle1": direction_data[i]["prcv_loc"],
			"angle2": direction_data[i+1]["prcv_loc"],
			"pcws1": direction_data[i]["pcws_before"][0],
			"pcws2": direction_data[i+1]["pcws_before"][0],
			"change": direction_data[i]["direction"]
			})
# now output should be roughly 10 * 5? :S debug pls! 
# print len(output)
# for j in range(0, subjects):
# 	print len(output[j])
print utils.DIRECTIONS[direction]
for k in range(0, len(output)):
	if pair < len(output[k]):
		print "Printing data for subject: ", k+1
		print "   Angle 1:"
		print "   ", output[k][pair]["angle1"]
		print "   Angle 2:"
		print "   ", output[k][pair]["angle2"]
		print "   PCW Set 1:"
		print "   ", np.array(output[k][pair]["pcws1"]).astype(np.int16)
		print "   PCW Set 2:"
		print "   ", np.array(output[k][pair]["pcws2"]).astype(np.int16)
		print "   Change directions!"
		print "   ", output[k][pair]["change"]