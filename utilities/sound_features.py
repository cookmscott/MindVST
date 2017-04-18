import glob
import os
import librosa
import librosa.display as libdisplay
import numpy as np
import matplotlib.pyplot as plt
# import tensorflow as tf
from matplotlib.pyplot import specgram


def load_sound_files(file_paths):
    raw_sounds = []
    for fp in file_paths:
        X,sr = librosa.load(fp)
        raw_sounds.append(X)
    return raw_sounds

# Set Plt Size
fig = plt.figure(figsize=(10,20))

def plot_waves(sound_names, raw_sounds):
    i = 1
    for n,f in zip(sound_names,raw_sounds):
        plt.subplot(6,1,i)
        libdisplay.waveplot(np.array(f),sr=22050)
        plt.title(n.title() + ' - Waveplot')
        i += 1

def plot_specgram(sound_names, raw_sounds):
    i = 1
    for n,f in zip(sound_names,raw_sounds):
        plt.subplot(6,1,i+2)
        specgram(np.array(f), Fs=22050)
        plt.title(n.title() + ' - Spectrogram')
        plt.colorbar(format='%+2.0f dB')
        i += 1

def plot_log_power_specgram(sound_names,raw_sounds):
    i = 1
    for n,f in zip(sound_names,raw_sounds):
        plt.subplot(6,1,i+4)
        D = librosa.logamplitude(np.abs(librosa.stft(f))**2, ref_power=np.max)
        libdisplay.specshow(D,x_axis='time' ,y_axis='log')
        plt.title(n.title() + ' - Log Power Spectrogram')
        plt.colorbar(format='%+2.0f dB')
        i += 1

def plot_full_set(wav_in, wav_out):

    sound_file_paths = [wav_in, wav_out]
    sound_names = ["wav_in", "wav_out"]
    raw_sounds = load_sound_files(sound_file_paths)

    plot_waves(sound_names, raw_sounds)
    plot_specgram(sound_names, raw_sounds)
    plot_log_power_specgram(sound_names, raw_sounds)

    plt.tight_layout()
    img = "/Users/scott.cook/PycharmProjects/MindVST/utilities/waves.png"
    fig.savefig(img)
