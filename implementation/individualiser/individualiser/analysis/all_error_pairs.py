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
	pair['angle1'] = a1
	pair['angle2'] = a2

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
print "Sorted datasets!"
print "up left len: ", len(up_left)
print "up right len: ", len(up_right)
print "down left len: ", len(down_left)
print "down right len: ", len(down_right)

print "Change data extracted!"
up_left_change = np.zeros([len(up_left), 10])
up_right_change = np.zeros([len(up_right), 10])
down_left_change = np.zeros([len(down_left), 10])
down_right_change = np.zeros([len(down_right), 10])

up_left_angle = np.zeros([len(up_left), 2])
up_right_angle = np.zeros([len(up_right), 2])
down_left_angle = np.zeros([len(down_left), 2])
down_right_angle = np.zeros([len(down_right), 2])

# sort just the change data into these arrays
# change array = pcw1 - pcw2

for n in range(0, len(up_left)):
	up_left_change[n] = np.array(up_left[n]['pcws1']) - np.array(up_left[n]['pcws2'])
	up_left_angle[n] = utils.fix_angles(up_left[n]['angle1'], up_left[n]['angle2'])
print up_left_change.shape

for x in range(0, len(up_right)):
	up_right_change[x] = np.array(up_right[x]['pcws1']) - np.array(up_left[x]['pcws2'])
	up_right_angle[x] = utils.fix_angles(up_right[x]['angle1'], up_right[x]['angle2'])
print up_right_change.shape

for p in range(0, len(down_left)):
	down_left_change[p] = np.array(down_left[p]['pcws1']) - np.array(down_left[p]['pcws2'])
	down_left_angle[p] = utils.fix_angles(down_left[p]['angle1'], down_left[p]['angle2'])
print down_left_change.shape

for q in range(0, len(down_right)):
	down_right_change[q] = np.array(down_right[q]['pcws1']) - np.array(down_right[q]['pcws2'])
	down_right_angle[q] = utils.fix_angles(down_right[q]['angle1'], down_right[q]['angle2'])
print down_right_change.shape

print up_left_change.transpose().shape
# plot.boxplot(up_left_change)
# plot.show()

# I could try to remove outliers by checking if the values
# in the angle array are above like 50
up_left_angle, up_left_change = utils.remove_outliers(up_left_angle, up_left_change)
up_right_angle, up_right_change = utils.remove_outliers(up_right_angle, up_right_change)
down_left_angle, down_left_change = utils.remove_outliers(down_left_angle, down_left_change)
down_right_angle, down_right_change = utils.remove_outliers(down_right_angle, down_right_change)

print "Average change values!"
up_left_average = utils.column_mean(up_left_change)
print up_left_average.shape
up_right_average = utils.column_mean(up_right_change)
print up_right_average.shape
down_left_average = utils.column_mean(down_left_change)
print down_left_average.shape
down_right_average = utils.column_mean(down_right_change)
print down_right_average.shape

print "Average angles!"
up_left_avg_ang = utils.column_mean(up_left_angle)
print up_left_avg_ang
up_right_avg_ang = utils.column_mean(up_right_angle)
print up_right_avg_ang
down_left_avg_ang = utils.column_mean(down_left_angle)
print down_left_avg_ang
down_right_avg_ang = utils.column_mean(down_right_angle)
print down_right_avg_ang

# prepare the plot
f, ((ax1, ax2), (ax3, ax4)) = plot.subplots(2, 2, sharex='col', sharey='row')
f.text(0.5, 0.04, 'Principal Component Weight', ha='center', va='center')
f.text(0.07, 0.5, "Change Value", ha='center', va='center', rotation='vertical')
# plot averages as dots
ax1.axis([1, 10, -3, 3])
ax2.axis([1, 10, -3, 3])
ax3.axis([1, 10, -3, 3])
ax4.axis([1, 10, -3, 3])
ax1.plot(up_left_average, 'rs')
ax1.set_title("Up/Left: " + np.array_str(up_left_avg_ang, precision=2))
ax2.plot(up_right_average, 'rs')
ax2.set_title("Up Right: " + np.array_str(up_right_avg_ang, precision=2))
ax3.plot(down_left_average, 'rs')
ax3.set_title("Down Left: " + np.array_str(down_left_avg_ang, precision=2))
ax4.plot(down_right_average, 'rs')
ax4.set_title("Down Right: " + np.array_str(down_right_avg_ang, precision=2))

# plot on violin/boxplots
# ax1.violinplot(up_left_change)
# ax2.violinplot(up_right_change)
# ax3.violinplot(down_left_change)
# ax4.violinplot(down_right_change)

plot.show()