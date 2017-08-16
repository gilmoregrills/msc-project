# fetch all error rates for a single direction
# and plot them on an appropriate chart??

import utils
import sys
import numpy as np 
import os
import scipy as scp 
import matplotlib.pyplot as plot 
import simplejson as json
import math

subjects = len(os.listdir("subjects"))

output = []

for direction in range(0, 8):
	# for sublist in range(0, subjects):
	# 	output.append([])
	for subject in range(1, subjects+1):
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
				"pcws1": direction_data[i]['pcws_before'][0],
				"pcws2": direction_data[i+1]['pcws_before'][0],
				"change": direction_data[i]['direction']
				})


print "total number of measurement pairs: ", len(output)

up_left = []
up_right = []
down_left = []
down_right = []

# now we will sort every dict in output
# into a list befitting the movement made
for pair in output:
	# make data marginally easier to work with
	a1 = pair['angle1']
	a2 = pair['angle2']
	if a1[1] > 90:
		a = a1[1] - 90 
		a1[1] = 90 - a
	if a2[1] > 90:
		b = a2[1] - 90
		a2[1] = 90 - b

	# if left or right
	if (abs(a1[0] - a2[0]) > 180):

		if (a2[0] < a1[0]):
			# right! now up or down?
			if (a2[1] < a1[1]):
				# down
				down_right.append(pair)
			elif (a2[1] > a1[1]):
				# up
				up_right.append(pair)

		elif (a2[0] > a1[0]):
			# left! now up or down?
			if (a2[1] < a1[1]):
				# down
				down_left.append(pair)
			elif (a2[1] > a1[1]):
				# up
				up_left.append(pair)

	elif (abs(a1[0] - a2[0]) < 180):

		if (a2[0] < a1[0]):
			# left! now up or down?
			if (a2[1] < a1[1]):
				# down
				down_left.append(pair)
			elif (a2[1] > a1[1]):
				# up
				up_left.append(pair)

		if (a2[0] > a1[0]):
			# right! now up or down?
			if (a2[1] < a1[1]):
				# down
				down_right.append(pair)
			elif (a2[1] > a1[1]):
				# up
				up_right.append(pair)

print "up left len: ", len(up_left)
print "up right len: ", len(up_right)
print "down left len: ", len(down_left)
print "down right len: ", len(down_right)

print up_right[0]