__author__ = 'scott.cook'

from hyperopt import fmin, tpe, hp, STATUS_OK
import subprocess
import time


def process_vst_and_compare(midi, plugin, p1, p2, wav_in, wav_out):
    cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s --parameter 4,%s --parameter 9,%s 1>&2'
    subprocess.Popen(cmd % (midi, wav_out, plugin, p1, p2), shell=True, stderr=subprocess.PIPE)
    time.sleep(0.4)
    cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/overlap-analysis %s %s | sed -n -e \'s/^.*Value of match was://p\' 1>&2'
    score = subprocess.Popen(cmd2 % (wav_in, wav_out), shell=True, stderr=subprocess.PIPE)
    time.sleep(0.4)
    return 1 - float(score.stderr.readline())

# SET NEEDED INPUT AND OUTPUT VARIABLES
midi = '/Users/scott.cook/PycharmProjects/MindVST/samples/midi_C4_16s_1.mid'
plugin = 'Obxd'
wav_in = '/Users/scott.cook/PycharmProjects/MindVST/samples/input.wav'
wav_out = '/Users/scott.cook/PycharmProjects/MindVST/samples/output.wav'


print "[INFO] Starting Param Optimization for %s..." % plugin

run_counter = 0

def run_wrapper(params):
    global run_counter
    run_counter += 1
    print "RUN %s" % run_counter

    score = run_test(params)

    print "  [INFO] SCORE: %s" % score
    print "\n"

    return score


def run_test(params):

    print  params[1]

    p1, p2 = params
    print("  [INFO] p1 = %s" % p1)
    print("  [INFO] p2 = %s" % p2)

    global midi
    global plugin
    global wav_in
    global wav_out

    score = process_vst_and_compare(midi, plugin, p1, p2, wav_in, wav_out)

    return score


space = (hp.uniform('p1', 0, 1),
         hp.uniform('p2', 0, 1))

best = fmin(run_wrapper,
            space,
            algo=tpe.suggest,
            max_evals=100)

print best
