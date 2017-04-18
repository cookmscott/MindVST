#!/usr/bin/python
import subprocess

def process_vst(midi, plugin, wav_out):
    wav_out = '/Users/scott.cook/PycharmProjects/MindVST/' + wav_out
    cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s --parameter 4,1'
    mrswatson_output = subprocess.Popen(cmd % (midi, wav_out, plugin), shell=True, stdout=subprocess.PIPE)
    return wav_out

def waveform_compare(wav1, wav2):
    # Run waveform-compare and grab stdout
    cmd = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/waveform-compare %s %s | sed -n -e \'s/^.*Value in block: //p\''
    score = subprocess.Popen(cmd % (wav1, wav2), shell=True, stdout=subprocess.PIPE)
    return float(score.stdout.readline())

midi = '/Users/scott.cook/Downloads/output_1.mid'
plugin = 'Obxd'
wav_out = 'new.wav'

waveform1 = '/Users/scott.cook/PycharmProjects/MindVST/input.wav'
waveform2 = '/Users/scott.cook/PycharmProjects/MindVST/output.wav'

score = waveform_compare(waveform1, waveform2)
wav_out = process_vst(midi, plugin, wav_out)

print('Current score: %s' % score)
print('VST output wav: %s' % wav_out)
print('DONE!')

###########################
# PLOT WAV FINAL WAV FILE #
###########################
# I SHOULD PUT THIS IN ANOTHER FILE / CLASS

from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi
from scipy.io.wavfile import read,write

def plotSpectru(y,Fs):
    n = len(y) # lungime semnal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    Y = fft(y)/n # fft computing and normalization
    Y = Y[range(n/2)]

    plot(frq,abs(Y),'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

Fs = 44100 # sampling rate

rate, data = read(wav_out)
y = data[:, 1]
lungime = len(y)
timp = len(y)/44100.
t = linspace(0, timp, len(y))

subplot(2, 1, 1)
plot(t, y)
xlabel('Time')
ylabel('Amplitude')
subplot(2, 1, 2)
plotSpectru(y, Fs)
show()
