import numpy as np
import scipy as scp
import scipy.signal as sig
import scipy.io.wavfile as wav
import pyaudio
import wave
import sys
import os
import subprocess
import time
import simplejson as json
import socket

while 1 == True:
	print "ready? yes/y or exit \n>"
	answer2 = raw_input()
	if answer2 == "yes" or answer2 == "y":
		print "fetching next source location and HRIR"
	elif answer2 == "exit":
		break

	# connect to individualiser
	host = "35.176.144.147"
	port = 54679
	sock = socket.socket()
	sock.connect((host, port))

	# fetching sound source position
	current_source = sock.recv(1024)
	current_source = json.loads(current_source)
	print "current source: ", current_source, type(current_source)

	# fetching size of input HRIR
	size = int(sock.recv(1024))
	print "size received: ", size

	# fetch the HRIR
	input_data = sock.recv(1024)
	while sys.getsizeof(input_data) < size:
		#print "receiving data", sys.getsizeof(input_data)
		input_data = input_data+sock.recv(1024)
	print "hrir data received \n", sys.getsizeof(input_data)

	# decode HRIR data from JSON to a normal array
	as_string = input_data.decode("utf-8")
	hrir = json.loads(as_string)

	# get left and right HRIRs for the current source direction
	hrir_l = hrir[0][current_source[0]][current_source[1]]
	hrir_r = hrir[1][current_source[0]][current_source[1]]

	# fetch input wave file
	pinknoise = wav.read('pinknoise.wav')

	# prepare output array, convolve input with 
	# each HRIR
	output = np.zeros([2, 44100])
	output[0] = sig.convolve(pinknoise[1], hrir_l, mode='same')
	output[1] = sig.convolve(pinknoise[1], hrir_r, mode='same')

	# write the output wave file!
	wav.write("output.wav", 44100, output.T)

	# now let's play it!
	while 1 == True:

		audiofile = "output.wav"
		FNULL = open(os.devnull, 'w')
		# open VLC, sleep while the sample plays, then terminate the process!
		player = subprocess.Popen(['vlc', '-vvv', audiofile], stdout=FNULL, stderr=subprocess.STDOUT)
		time.sleep(1.2)
		player.kill()
		player.terminate()
		player.wait()

		# confirm, play again? if no, break 
		# out and return to main loop
		print "play the sample again? \n>"
		answer1 = raw_input()
		if answer1 == "no" or answer1 == "n":
			break 
		else: 
			continue


