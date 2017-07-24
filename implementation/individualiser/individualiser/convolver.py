import numpy as np
import scipy as scp
import scipy.signal as sig
import scipy.io.wavfile as wav
import lmdb_interface as lmdb
import utility_functions as util
import pyaudio
import wave
import sys
import os
import subprocess
import time
import simplejson as json
import socket

while 1 == True:
	# fetch data from individualiser
	host = "35.176.144.147"
	port = 54679

	sock = socket.socket()

	sock.connect((host, port))
	current_source = sock.recv(1024)
	print current_source
	current_source = json.loads(current_source)
	print "current source: ", current_source, type(current_source)
	size = int(sock.recv(1024))
	print "size received: ", size
	input_data = sock.recv(1024)
	while sys.getsizeof(input_data) < size:
		#print "receiving data", sys.getsizeof(input_data)
		input_data = input_data+sock.recv(1024)
	print "hrir data received \n", sys.getsizeof(input_data)
	as_string = input_data.decode("utf-8")
	hrir = json.loads(as_string)
	# run from AWS for now, fetch via socket later
	# hrir = lmdb.fetch('custom_hrir')
	# sound_src = lmdb.fetch('current_source')

	hrir_l = hrir[0][current_source[0]][current_source[1]]
	hrir_r = hrir[1][current_source[0]][current_source[1]]

	pinknoise = wav.read('pinknoise.wav')

	output = np.zeros([2, 44100])
	output[0] = sig.convolve(pinknoise[1], hrir_l, mode='same')
	output[1] = sig.convolve(pinknoise[1], hrir_r, mode='same')

	wav.write("output.wav", 44100, output.T)
	while 1 == True:
		audiofile = "output.wav"

		FNULL = open(os.devnull, 'w')

		player = subprocess.Popen(['vlc', '-vvv', audiofile], stdout=FNULL, stderr=subprocess.STDOUT)
		time.sleep(1.2)
		player.kill()
		player.terminate()
		player.wait()
		print "Would you like to play the sample again?"
		answer1 = raw_input()
		if answer1 is "no" or answer1 is "n":
			break 

	print "ready for the next sample?"
	answer2 = raw_input()
	if answer2 is "yes" or answer2 is "y":
			break 

