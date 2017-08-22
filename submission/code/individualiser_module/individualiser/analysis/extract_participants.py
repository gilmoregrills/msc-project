# pass date, start datetime, end datetime, and participant ID at run
# format: DD-MM-YYYY, HH-MM-SS *2, and an int 
# script should extract that information into a new JSON
# file for that subject ready for use by other scripts

import simplejson as json 
import os
import sys
from datetime import datetime, timedelta

date = sys.argv[1]
start_time = datetime.strptime(sys.argv[2], "%H-%M-%S")
end_time = datetime.strptime(sys.argv[3], "%H-%M-%S")
participant = sys.argv[4]

print "isolating data from: ", date, start_time, end_time, participant

log_path = "../logs/" + date + "/log.json"
out_path = "subjects/"+participant+".json"

print "logs being fetched from: ", log_path

# open log file, load from json to object, close file
file = open(log_path, "r")
logs = json.loads(file.read())['logs']
print "loaded in a ", type(logs), " of ", len(logs), " logs"
file.close()

# prepare output dict 
output = {
	"subject": participant,
	"data": []
}

# iterate through logs, if between start datetime and end datetime add 
# to output, unless it's within 3-5 seconds of the previous datetime
# then assign current log timestampt to previous datetime
previous_time = None
for log in logs:
	timestamp = datetime.strptime(log['timestamp'], "%H-%M-%S")
	
	if timestamp >= start_time and timestamp <= end_time \
			and ((previous_time == None) \
			or (timestamp - previous_time > timedelta(seconds=2))):
		output['data'].append(log)
	previous_time = timestamp


print "number of valid logs: ", len(output['data'])

if len(output['data']) > 48:
	beheadings = len(output['data']) - 48
	print "removing ", beheadings, " practice logs from data"
	for head in range(0, beheadings):
		output['data'].pop(0)

print "final output len: ", len(output['data'])

out_file = open(out_path, "w")
out_file.write(json.dumps(output, indent=4, sort_keys=True))
out_file.close()