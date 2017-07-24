import numpy as np
import scipy as scp
import scipy.signal as sig
import scipy.io.wavfile as wav
import lmdb_interface as lmdb
import pyaudio
import wave
import sys
import os
import subprocess
import time

hrir = lmdb.fetch('custom_hrir')
hrir_l = hrir[0][0][0]
hrir_r = hrir[1][0][0]

pinknoise = wav.read('pinknoise.wav')

output = np.zeros([2, 44100])
output[0] = sig.convolve(pinknoise[1], hrir_l, mode='same')
output[1] = sig.convolve(pinknoise[1], hrir_r, mode='same')

wav.write("output.wav", 44100, output.T)

audiofile = "output.wav"

FNULL = open(os.devnull, 'w')

player = subprocess.Popen(['vlc', '-vvv', audiofile], stdout=FNULL, stderr=subprocess.STDOUT)
time.sleep(1.2)
player.kill()
player.terminate()
player.wait()

