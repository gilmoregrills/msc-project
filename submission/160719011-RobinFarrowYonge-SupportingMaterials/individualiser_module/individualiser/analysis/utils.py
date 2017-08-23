# helpful functions and data! Excuse the lack of documentation! I'm dying!!!
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

# fetch an 8x6x2 array of error data for one
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

	for errs in output:
		while len(errs) < 6:
			errs.append([0.0, 0.0])
		while len(errs) > 6:
			errs.pop(0)

	output = np.array(output)
	return output


# errors should be a single subject's 
# error data in the shape 8*6*2
def sum_errors(errors):
	dim1 = len(errors)
	dim2 = len(errors[0])

	output = np.zeros([dim1, dim2])
	output.flags.writeable = True

	for direction in range(0, dim1):
		for error in range(0, dim2):

			error_sum = abs(errors[direction][error][0]) + abs(errors[direction][error][1])
			output[direction][error] = error_sum
	
	return output


# fetch a SUBJECTS * 6 * 2 array that contains
# each subject's errors for a given direction 
def fetch_all_for_direction(direction):
	subjects = len(os.listdir("subjects"))
	output = np.zeros([subjects, 6, 2])

	for subject in range(1, subjects+1):
		if subject != 2:
			all_errors = fetch_individual_errors(subject)
			output[subject-1] = all_errors[direction]

	return output

# takes a 2D array, and returns the column mean
# of the data! So if all of the results for a 
# direction was the input, it would return the
# mean error rate for that direction
def column_mean(input_data):
	dim1 = len(input_data)
	dim2 = len(input_data[0])
	output = np.zeros([dim2])

	for column in range(0, dim2):
		avg = 0
		counter = 1
		for row in range(0, dim1):
			if input_data[row][column] != 0.0:
				avg += input_data[row][column]
				counter += 1
				# print counter

		avg = avg / dim1
		output[column] = avg

	return output

# print "EACH PARTICIPANT OVER ALL DIRECTIONS"
# for hats in range(1, 11):
# 	print hats
# 	testo = fetch_individual_errors(hats)
# 	testo = sum_errors(testo)
# 	print column_mean(testo)
# print "FOR ALL PARTICIPANTS IN A DIRECTION"
# for butts in range(0, 8):
# 	print butts
# 	testo2 = fetch_all_for_direction(butts)
# 	testo2 = sum_errors(testo2)
# 	print column_mean(testo2)

def fix_angles(angle1, angle2):

	output = np.array([1, 2])
	output[1] = abs(angle1[1] - angle2[1])
	
	tmp = angle1[0] - angle2[0]
	if abs(tmp) > 180:
		output[0] = 360 - abs[tmp]
	else: 
		output[0] = abs(tmp)

	return output


def remove_outliers(angles, changes):
	to_delete = []
	count = 0
	for anglepair in angles:
		if anglepair[0] > 80 or anglepair[1] > 80:
			to_delete.append(count)
		count += 1

	print to_delete

	out_angle = np.delete(angles, to_delete, axis=0)
	out_change = np.delete(changes, to_delete, axis=0)

	print "removed ", len(angles) - len(out_angle), " records"
	
	return out_angle, out_change