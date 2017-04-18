""" THIS ATTEMPT USES ALL PARAMS FROM Obxd
"""

import csv

# get csv of param info from running the following:
# /Users/scott.cook/Documents/MrsWatson/main/mrswatson -p Obxd --display-info

# file should be of format:
# param num,param name,param value
reader = csv.reader(open('vst_params/Obxd_params.csv'))

from hyperopt import fmin, tpe, hp
import subprocess
import time
import os.path
import sys

def process_vst_and_compare(midi, plugin, vst_params, wav_in, wav_out):
    cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s %s 1>&2'
    subprocess.Popen(cmd % (midi, wav_out, plugin, vst_params), shell=True, stderr=subprocess.PIPE)
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

# ENSURE ALL FILES EXISTS

if os.path.exists(midi):
    print "Midi: %s" % midi
else:
    print "Midi %s does not exist" % midi
    sys.exit()

if os.path.exists(wav_in):
    print "wav_in: %s" % wav_in
else:
    print "wav_in %s does not exist" % wav_in
    sys.exit()

if os.path.exists(wav_out):
    print "wav_out: %s" % wav_out
else:
    print "wav_out %s does not exist" % wav_out
    sys.exit()

print "[INFO] Starting Param Optimization for %s..." % plugin
log = open("log.txt", "w")

"""
Define and run hyperparameter optimization on
parameter space for given plugin
"""

run_counter = 0

def run_wrapper(params):
    global run_counter
    run_counter += 1
    print "RUN %s" % run_counter
    log.write("RUN %s\n" % run_counter)

    print len(params)

    score = run_test(params)

    print "  [INFO] SCORE: %s" % score
    print "\n"
    log.write("  [INFO] SCORE: %s\n" % score)

    return score


def run_test(params):

    print "HELLO FIRST PARAM %s" % params[0]

    # params start at [0] but plugins params start with 1 so I add +1 to param iterations
    vst_params = ''
    for i in xrange(len(params)):
        vst_params += " --parameter %s,%s" % (i+1, params[i])

    print("  [INFO] vst_params = %s" % vst_params)
    log.write("  [INFO] vst_params = %s\n" % vst_params)

    global midi
    global plugin
    global wav_in
    global wav_out

    score = process_vst_and_compare(midi, plugin, vst_params, wav_in, wav_out)

    return score


space = (
    hp.uniform('p1',0,1),
    hp.uniform('p2',0,1),
    hp.uniform('p3',0,1),
    hp.uniform('p4',0,1),
    hp.uniform('p5',0,1),
    hp.uniform('p6',0,1),
    hp.uniform('p7',0,1),
    hp.uniform('p8',0,1),
    hp.uniform('p9',0,1),
    hp.uniform('p10',0,1),
    hp.uniform('p11',0,1),
    hp.uniform('p12',0,1),
    hp.uniform('p13',0,1),
    hp.uniform('p14',0,1),
    hp.uniform('p15',0,1),
    hp.uniform('p16',0,1),
    hp.uniform('p17',0,1),
    hp.uniform('p18',0,1),
    hp.uniform('p19',0,1),
    hp.uniform('p20',0,1),
    hp.uniform('p21',0,1),
    hp.uniform('p22',0,1),
    hp.uniform('p23',0,1),
    hp.uniform('p24',0,1),
    hp.uniform('p25',0,1),
    hp.uniform('p26',0,1),
    hp.uniform('p27',0,1),
    hp.uniform('p28',0,1),
    hp.uniform('p29',0,1),
    hp.uniform('p30',0,1),
    hp.uniform('p31',0,1),
    hp.uniform('p32',0,1),
    hp.uniform('p33',0,1),
    hp.uniform('p34',0,1),
    hp.uniform('p35',0,1),
    hp.uniform('p36',0,1),
    hp.uniform('p37',0,1),
    hp.uniform('p38',0,1),
    hp.uniform('p39',0,1),
    hp.uniform('p40',0,1),
    hp.uniform('p41',0,1),
    hp.uniform('p42',0,1),
    hp.uniform('p43',0,1),
    hp.uniform('p44',0,1),
    hp.uniform('p45',0,1),
    hp.uniform('p46',0,1),
    hp.uniform('p47',0,1),
    hp.uniform('p48',0,1),
    hp.uniform('p49',0,1),
    hp.uniform('p50',0,1),
    hp.uniform('p51',0,1),
    hp.uniform('p52',0,1),
    hp.uniform('p53',0,1),
    hp.uniform('p54',0,1),
    hp.uniform('p55',0,1),
    hp.uniform('p56',0,1),
    hp.uniform('p57',0,1),
    hp.uniform('p58',0,1),
    hp.uniform('p59',0,1),
    hp.uniform('p60',0,1),
    hp.uniform('p61',0,1),
    hp.uniform('p62',0,1),
    hp.uniform('p63',0,1),
    hp.uniform('p64',0,1),
    hp.uniform('p65',0,1),
    hp.uniform('p66',0,1),
    hp.uniform('p67',0,1),
    hp.uniform('p68',0,1),
    hp.uniform('p69',0,1),
    hp.uniform('p70',0,1),
    hp.uniform('p71',0,1),
    hp.uniform('p72',0,1),
    hp.uniform('p73',0,1),
    hp.uniform('p74',0,1),
    hp.uniform('p75',0,1),
    hp.uniform('p76',0,1),
    hp.uniform('p77',0,1),
    hp.uniform('p78',0,1),
    hp.uniform('p79',0,1))

best = fmin(run_wrapper,
            space,
            algo=tpe.suggest,
            max_evals=1000)

print best

log.close()