import sys
from mido import Message, MetaMessage, MidiFile, MidiTrack

mid = MidiFile(type=0)
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=0, time=0))
track.append(Message('note_on', note=57, velocity=100, time=0))
track.append(Message('note_off', note=57, velocity=100, time=2800))

mid.save('/Users/scott.cook/PycharmProjects/MindVST/samples/midi_A3_3s.mid')


filename = '/Users/scott.cook/PycharmProjects/MindVST/samples/midi_A3_3s.mid'

midi_file = MidiFile(filename)

for i, track in enumerate(midi_file.tracks):
    sys.stdout.write('=== Track {}\n'.format(i))
    for message in track:
        sys.stdout.write('  {!r}\n'.format(message))
