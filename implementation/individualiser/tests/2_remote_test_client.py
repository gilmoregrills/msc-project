import sys
import socket
import simplejson as json
import time
import os

host = "127.0.0.1"
port = 8080

sock = socket.socket()

sock.connect((host, port))
input_data = sock.recv(1024)
while sys.getsizeof(input_data) < 5545907:
	input_data = input_data+sock.recv(1024)
print "hrtf data received \n", sys.getsizeof(input_data)
as_string = input_data.decode("utf-8")
#print "data as a string: \n", as_string
hrtf_data = json.loads(as_string)
filename = "testhrtfs/hrtf_as_json_"+time.strftime("%H-%M-%S")+"_"+time.strftime("%d-%m-%Y")+".json"
hrtf_data_file = open(filename, "w")
hrtf_data_file.write(json.dumps(hrtf_data, indent=4, sort_keys=True))
hrtf_data_file.close()
print "data translated from JSON to array of shape: ", len(hrtf_data), len(hrtf_data[0]), len(hrtf_data[0][0]), len(hrtf_data[0][0][0])

sock.close()
