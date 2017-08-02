import sys
from mido import Message, MetaMessage, MidiFile, MidiTrack

mid = MidiFile(type=0)
track = MidiTrack()
mid.tracks.append(track)

note = 46

track.append(Message('program_change', program=0, time=0))
track.append(Message('note_on', note=note, velocity=100, time=0))
track.append(Message('note_off', note=note, velocity=100, time=900))


mid.save('/Users/scott.cook/PycharmProjects/MindVST/samples/midi_files/midi_As3_900ms.mid')


filename = '/Users/scott.cook/PycharmProjects/MindVST/samples/midi_files/midi_As3_900ms.mid'

midi_file = MidiFile(filename)

for i, track in enumerate(midi_file.tracks):
    sys.stdout.write('=== Track {}\n'.format(i))
    for message in track:
        sys.stdout.write('  {!r}\n'.format(message))
