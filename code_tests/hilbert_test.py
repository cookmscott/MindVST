
import librosa
import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt

def load_sound_files(file_paths):
    raw_sounds = []
    for fp in file_paths:
        X,sr = librosa.load(fp, mono=True)
        print "Filepath: %s has sample rate of %s and duration %s" % (fp,sr,librosa.get_duration(X, sr))
        raw_sounds.append(X)
    return raw_sounds

wav_in = "/Users/scott.cook/PycharmProjects/MindVST/samples/test_runs/test_9/input.wav"
wav_out = "/Users/scott.cook/PycharmProjects/MindVST/samples/test_runs/test_9/output_0.529.wav"

# only plotting one raw_sounds[1] wav file input.wav
sound_file_paths = [wav_in, wav_out]
raw_sounds = load_sound_files(sound_file_paths)
signal = np.array(raw_sounds[1])
print len(signal)


duration =2.53097505669
fs = 22050
samples = int(fs*duration)
t = np.arange(samples) / fs
print(t)
print len(t)

# The amplitude envelope is given by magnitude of the analytic signal. The
# instantaneous frequency can be obtained by differentiating the
# instantaneous phase in respect to time. The instantaneous phase corresponds
# to the phase angle of the analytic signal.
analytic_signal = hilbert(signal)
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.unwrap(np.angle(analytic_signal))
instantaneous_frequency = (np.diff(instantaneous_phase) /
                           (2.0*np.pi) * fs)

#plt.plot(amplitude_envelope)
#plt.show()

plt.plot(amplitude_envelope)
plt.plot(signal)
plt.show()


"""
fig = plt.figure()
ax0 = fig.add_subplot(211)
ax0.plot(signal, label='signal')
ax0.plot(amplitude_envelope, label='envelope')
ax0.set_xlabel("time in seconds")
ax0.legend()
ax1 = fig.add_subplot(212)
ax1.plot(t[1:], instantaneous_frequency)
ax1.set_xlabel("time in seconds")
ax1.set_ylim(0.0, 120.0)

img = "/Users/scott.cook/PycharmProjects/MindVST/code_tests/hilbert_test.png"
"""