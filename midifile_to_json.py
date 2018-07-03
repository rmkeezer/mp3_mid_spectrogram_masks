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


def draw_shape(image, shape, dims, color):
    # Get the center x, y and the size s
    x, y, s = dims
    image = cv2.circle(image, (x, y), s, color, -1)
    return image

a = 440
midfreq = [(a / 32) * (2 ** ((x - 9) / 12)) for x in range(0, 128)]

hzbin = 22050.0 / 1024.0

import os
for fn in os.listdir('./midis/midi'):
    if fn.endswith(".mid"):
        print(fn)
        fn = fn[:-4]
        mid = mido.MidiFile('./midis/midi/' + fn + '.mid')

        currentTime = 0
        channels = {}
        for msg in mid:
            currentTime += msg.time
            if msg.type == 'program_change':
                if channels.get(msg.channel) != None and msg.time != 0:
                    print("BAD CHANNEL CHANGE")
                    asdf
                channels[msg.channel] = ([],msg.program)
            if msg.type == 'note_on':
                if msg.velocity != 0:
                    channels[msg.channel][0].append((currentTime, msg.note))
        with open('test.json','w') as f:
            f.write(json.dumps(channels, indent=2))


        for sec in range(0, int(mid.length), 1):

            if os.path.isfile('1secmidsSpec/' + fn + '_' + str(sec) + '_mask.npz'):
                continue

            notes = [n for n in channels[0][0] if n[0] >= sec and n[0] < sec + 1]

            import numpy as np
            import cv2
            from imageio import imwrite

            count = len(notes)
            mask = np.zeros([256, 329, count], dtype=np.uint8)
            for i, note in enumerate(notes):
                posy = int(midfreq[note[1]] / hzbin)
                posx = int(((note[0]%1)) * 329)
                mask[:, :, i] = draw_shape(mask[:, :, i].copy(),
                                                        'circle', (posx, posy, 10), 255)
            if count == 0:
                mask = np.zeros([256, 329, 1], dtype=np.uint8) 
            # Handle occlusions
            occlusion = np.logical_not(mask[:, :, -1]).astype(np.uint8)
            for i in range(count - 2, -1, -1):
                mask[:, :, i] = mask[:, :, i] * occlusion
                occlusion = np.logical_and(
                    occlusion, np.logical_not(mask[:, :, i]))
            # Map class names to class IDs.
            class_ids = np.array([n[1] for n in notes])

            #np.save('1secmidsSpec/' + fn + '_' + str(sec) + '_mask.npy', mask)
            np.savez_compressed('1secmidsSpec/' + fn + '_' + str(sec) + '_mask.npz', mask=mask)
            np.save('1secmidsSpec/' + fn + '_' + str(sec) + '_notes.npy', notes)
            # imwrite('1secmidsSpec/' + fn + '_' + str(sec) + '_mask.png', mask[:,:,0])
            # for i, note in enumerate(notes):
            #     imwrite('1secmidsSpec/masks/' + fn + '_' + str(sec) + '_' + str(i) + '_' + str(note[1]) + '_mask.png', mask[:,:,i])