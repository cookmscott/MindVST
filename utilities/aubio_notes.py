#! /usr/bin/env python

"""
aubio notes is a utility for finding midi notes associated to frequency of audio input
win_s and hop_s affect the "threshold" at which individual notes are assessed
"""

import sys
from aubio import source, notes

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

downsample = 1
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

win_s = 512 // downsample # fft size
hop_s = 256 // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

notes_o = notes("default", win_s, hop_s, samplerate)

print("%8s" % "time","[ start","vel","last ]")

# total number of frames read
total_frames = 0
note_list = []
while True:
    samples, read = s()
    new_note = notes_o(samples)
    if (new_note[0] != 0):
        note_str = ' '.join(["%.2f" % i for i in new_note])
        note_list.append(note_str.split())
        print("%.6f" % (total_frames/float(samplerate)), new_note)
    total_frames += read
    if read < hop_s: break

midi_notes = [item[0] for item in note_list]
print midi_notes

'''
command line example:
aubionotes --input /Users/scott.cook/PycharmProjects/MindVST/samples/engine.wav --onset-threshold 0.1 --verbose
'''
aubionotes --input /Users/scott.cook/PycharmProjects/MindVST/samples/cello.wav --onset-threshold 0.1 --verbose
aubionotes --input /Users/scott.cook/PycharmProjects/MindVST/samples/generator_hum.wav --onset-threshold 0.1 --verbose