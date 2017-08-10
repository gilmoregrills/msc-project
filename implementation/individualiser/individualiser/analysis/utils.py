# helpful functions and data! 
import simplejson as json
import os
import sys
import numpy as np
from datetime import datetime, timedelta
import math

DIRECTIONS = [[45.0, 225.0], [-45.0, 225.0], 
			  [45.0, 45.0], [-45.0, 45.0], 
			  [-45.0, -45.0], [45.0, -45.0], 
			  [-45.0, 135.0], [45.0, 135.0]]

# fetch an 8x6 array of error data for one
# subject representing source positions and 
# localisation attempts
def fetch_individual_errors(subject):
	# prepare output structure
	output = [[], [], [], [], [], [], [], []]
	#output.flags.writable = True

	subject_path = "subjects/" + str(subject) + ".json"
	# open file
	file = open(subject_path, "r")
	# get data
	data = json.loads(file.read())['data']

	for entry in data:
		direction = entry['src_loc']
		index = DIRECTIONS.index(direction)
		errors = entry['error']
		if math.isnan(errors[0]):
			errors[0] = 0
		elif math.isnan(errors[1]):
			errors[1] = 0
		output[index].append(entry['error'])

	return output


fetch_individual_errors(2)