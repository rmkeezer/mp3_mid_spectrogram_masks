
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

stft_total = []
w = 0
i = 0
for fn in os.listdir('out/songparts/1sec/'):
    if fn.endswith(".wav"):
        try:
            print(fn)

            if os.path.isfile('out/specs/1sec/' + fn +'.png'.format(str(w).zfill(3))):
                continue

            input_signal = audio_utilities.get_signal('out/songparts/1sec/' + fn, expected_fs=44100)
            fft_size = 2048
            hopsamp = fft_size // 16
            stft_full = audio_utilities.stft_for_reconstruction(input_signal,
                                                                fft_size, hopsamp)

            stft_mag = abs(stft_full)
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
            # np.save('1secdone/' + fn[:-4] + 'n' + str(w), out)
            stft_mag = stft_mag[:, :256]
            #print(stft_mag.shape)
            
            imwrite('out/specs/1sec/' + fn +'.png'.format(str(w).zfill(3)), stft_mag.T)
            stft_total = []
            # i = 0
            w += 1
        except Exception as e:
            print(e)
            continue