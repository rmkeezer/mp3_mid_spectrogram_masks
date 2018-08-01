
import warnings
warnings.simplefilter("ignore")

import argparse
from pylab import *
import os

import numpy as np
from imageio import imwrite

import griffin_lim.audio_utilities as audio_utilities
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import sys

import librosa

stft_total = []
w = 0
i = 0
outfn = 'out/specs/6secSuperUHQ2/'
infn = 'out/songparts/6sec/'

def stft(x, fft_size, hopsamp):
    window = np.hanning(fft_size)
    return np.array([np.fft.rfft(window*x[i:i+fft_size])
                     for i in range(0, len(x)-fft_size, hopsamp)])

for fn in os.listdir(infn):
    if fn.endswith(".wav"):
        try:
            print(fn)

            fn = fn[:-4]

            if os.path.isfile(outfn + fn + '.png'.format(str(w).zfill(3))):
                continue

            input_signal = audio_utilities.get_signal(infn + fn + '.wav', expected_fs=44100)
            #input_signal, sample_rate = librosa.load(infn + 'aazitah.mp3', sr=44100)            
            
            #input_signal = input_signal[:1000000]

            fft_size = 8192
            hopsamp = fft_size // 16
            stft_full = stft(input_signal, fft_size, hopsamp)

            stft_mag = abs(stft_full)
            stft_mag = (stft_mag - np.mean(stft_mag)) / np.std(stft_mag)
            stft_mag += abs(np.min(stft_mag))
            stft_mag *= 255.0/np.max(stft_mag)
            # scale = 1.0 / np.amax(stft_mag)
            # stft_mag *= scale
            #stft_total.append(stft_mag)
            # i += 1
            # if i > 100:
            #     np.save('test' + str(w), np.array(stft_total))
            #     stft_total = []
            #     i = 0
            #     w += 1
            #out = np.dstack((stft_full.real, stft_full.imag))
            # np.save('1secdone/' + fn + 'n' + str(w), out)
            stft_mag = stft_mag[:, :512]
            #print(stft_mag.shape)
            
            imwrite(outfn + fn + '.png'.format(str(w).zfill(3)), stft_mag.T)
            stft_total = []
            # i = 0
            w += 1
        except Exception as e:
            print(e)
            continue