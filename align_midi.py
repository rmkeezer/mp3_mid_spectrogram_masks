
import warnings
warnings.simplefilter("ignore")

import argparse
from pylab import *
import os

import numpy as np
from imageio import imwrite

from griffin_lim import audio_utilities
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import sys

import json
import mido


def midifile_to_dict(mid):
    tracks = []
    for track in mid.tracks:
        tracks.append([vars(msg).copy() for msg in track])

    return {
        'ticks_per_beat': mid.ticks_per_beat,
        'tracks': tracks,
    }

stft_total = []
infn = 'in/songswithmidsALL/'
for fn in os.listdir(infn + 'wavs/'):
    if fn.endswith(".wav"):
        print(fn)
        input_signal = audio_utilities.get_signal(infn + 'wavs/' + fn, expected_fs=44100)
        fn = fn[:-4]
        try:
            mid = mido.MidiFile(infn + 'oldmidis/' + fn + '.mid')
        except Exception as e:
            print(e)
            continue
        # middict = midifile_to_dict(mid)
        # with open('test.json','w') as f:
        #     f.write(json.dumps(middict, indent=2))

        start = -1
        for i in range(input_signal.shape[0]):
            if sum(input_signal[i]) > 0.01:
                start = i
                break
        timeToStart = start / 44100.0
        tempo = -1
        time = -1
        print(timeToStart)
        for i, track in enumerate(mid.tracks):
            for i in range(len(track)):
                msg = track[i]
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                    break
                if msg.type == "note_on":
                    if time == -1 or msg.time < time:
                        time = msg.time
                    break
        currentTimeStarted = (time / mid.ticks_per_beat) * tempo / 1000000
        print(currentTimeStarted)
        tickDelay = int((((timeToStart - currentTimeStarted) * 1000000) / 500000) * mid.ticks_per_beat)
        tickSkip = int((((timeToStart - currentTimeStarted) * 1000000) / tempo) * mid.ticks_per_beat)
        print(tickDelay)
        print(tickSkip)
        firstTemp = True
        try:
            for i, track in enumerate(mid.tracks):
                for i in range(len(track)):
                    msg = track[i]
                    if msg.type == "set_tempo":
                        print(msg)
                        if tickDelay >= 0:
                            msg.time += tickDelay
                            track.insert(i,mido.MetaMessage('set_tempo',time=0,tempo=500000))
                            break
                        else:
                            if not firstTemp:
                                msg.time += tickSkip
                                if msg.time < 0:
                                    print("BELOW ZERO")
                                    tickSkip = msg.time
                                    print(tickSkip)
                                    msg.time = 0
                                    continue
                                break
                            firstTemp = False
                    if msg.type == "note_on":
                        print(msg)
                        if tickDelay >= 0:
                            msg.time += tickDelay
                        else:
                            msg.time += tickSkip
                        if msg.time < 0:
                            asjdkfas
                        break
        except Exception as e:
            print(e)
            continue
        if tickDelay < 0:
            middict = midifile_to_dict(mid)
            with open('test.json','w') as f:
                f.write(json.dumps(middict, indent=2))
        try:
            mid.save(infn + 'midis/' + fn + '.mid')
        except Exception as e:
            print(e)
            continue