import sys
import json
import mido
import os

import numpy as np
import cv2
from imageio import imwrite


def midifile_to_dict(mid):
    tracks = []
    for track in mid.tracks:
        tracks.append([vars(msg).copy() for msg in track])

    return {
        'ticks_per_beat': mid.ticks_per_beat,
        'tracks': tracks,
    }


def draw_shape(image, shape, dims, color):
    # Get the center x, y and the size s
    x, y, s = dims
    image = cv2.circle(image, (x, y), s, color, -1)
    return image

a = 440
midfreq = [(a / 32) * (2 ** ((x - 9) / 12)) for x in range(0, 128)]

fft_size = 8192
hzbin = 22050.0 / (fft_size / 2)

infn = 'in/songswithmids/midis/'
outfnMask = 'out/masks/6secSuperUHQ2/'
for fn in os.listdir(infn):
    if fn.endswith(".mid"):
        print(fn)
        fn = fn[:-4]
        
        mid = mido.MidiFile(infn + fn + '.mid')


        currentTime = 0
        channels = {}
        # for track in mid.tracks:
        #     channels[track.name] = []
        #     for msg in track:
        #         channels[track.name].append(msg.dict())
        try:
            for msg in mid:
                currentTime += msg.time
                if msg.type == 'program_change':
                    if channels.get(msg.channel) != None and msg.time != 0:
                        print("BAD CHANNEL CHANGE")
                        asdf
                    channels[msg.channel] = ([],msg.program)
                if msg.type == 'note_on':
                    if channels.get(msg.channel) == None:
                        channels[msg.channel] = ([],0)
                    if msg.velocity != 0:
                        channels[msg.channel][0].append((currentTime, msg.note, 1, msg.velocity))
                    else:
                        for i in range(len(channels[msg.channel][0])):
                            onnote = channels[msg.channel][0][-(i+1)]
                            if onnote[1] == msg.note:
                                channels[msg.channel][0][-(i+1)] = (onnote[0], onnote[1], currentTime-onnote[0], onnote[3])
                                break
        except Exception as e:
            print(e)
            print("BAD MID")
            os.rename(infn + fn + '.mid', infn + 'bad/' + fn + '.mid')
            continue
        # with open('test.json','w') as f:
        #     f.write(json.dumps(channels, indent=2))


        stride = 6
        pixWidth = 501
        pixHeight = 512
        radius = 4 #(note[3] // 10)
        for sec in range(0, int(mid.length), stride):

            if os.path.isfile(outfnMask + fn + '_' + str(sec) + '_mask.npz'):
                continue

            notechannels = []
            maskchannels = []
            for j in channels.keys():
                notes = [n for n in channels[j][0] if n[0] >= sec and n[0] < sec + stride]

                count = len(notes)
                mask = np.zeros([pixHeight, pixWidth, max(count, 1)], dtype=np.uint8)
                print(str(j) + ":" + str(sec))
                for i, note in enumerate(notes):
                    posy = int(midfreq[note[1]] / hzbin)
                    posx = int(((note[0]%stride)/stride) * pixWidth)
                    #print(note[0])
                    endposx = int(note[2]/stride * pixWidth)
                    mask[:, :, i] = draw_shape(mask[:, :, i].copy(),
                                                            'circle', (posx, posy, radius), 255)
                    mask[:, :, i] = cv2.rectangle(mask[:, :, i].copy(),(posx,posy-radius),(min(posx+endposx,pixWidth),posy+radius), 255, -1)
                notechannels.append((notes,channels[j][1]))
                maskchannels.append((mask, channels[j][1]))
            # Handle occlusions
            # occlusion = np.logical_not(mask[:, :, -1]).astype(np.uint8)
            # for i in range(count - 2, -1, -1):
            #     mask[:, :, i] = mask[:, :, i] * occlusion
            #     occlusion = np.logical_and(
            #         occlusion, np.logical_not(mask[:, :, i]))
            # Map class names to class IDs.
            class_ids = np.array([n[1] for n in notes])

            #np.save(outfnMask + fn + '_' + str(sec) + '_mask.npy', mask)
            np.savez_compressed(outfnMask + fn + '_' + str(sec) + '_mask.npz', mask=maskchannels)
            np.save(outfnMask + fn + '_' + str(sec) + '_notes.npy', notechannels)
            #imwrite(outfnMask + fn + '_' + str(sec) + '_mask.png', mask[:,:,0])
            # for i in range(len(mask[0,0])):
            #     imwrite(outfnMask + fn + '_' + str(sec) + '_' + str(i) + '_mask.png', mask[:,:,i])
            # for i, note in enumerate(notes):
            #     imwrite(outfnMask + fn + '_' + str(sec) + '_' + str(i) + '_' + str(note[1]) + '_mask.png', mask[:,:,i])

        os.rename(infn + fn + '.mid', infn + 'done/' + fn + '.mid')