__author__ = 'scott.cook'
""" THIS ATTEMPT USES **PARTIAL** FROM Spire
 >> specifically, this will only use two oscillators
 >> pulls from Spire-1.1_params_subset.csv
"""

from utilities import sound_features
from hyperopt import fmin, tpe, hp, rand
import subprocess
import time
import os.path
import sys
import csv

def files_exist(midi, wav_in, wav_out):
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

def process_vst_and_compare(midi, plugin, vst_params, wav_in, wav_out):
    try:
        cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s %s 1>&2'
        subprocess.Popen(cmd % (midi, wav_out, plugin, vst_params), shell=True, stderr=subprocess.PIPE)
        time.sleep(0.1)
        # cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/waveform-compare %s %s | sed -n -e \'s/^.*Value in block: //p\' 1>&2'
        cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/overlap-analysis %s %s | sed -n -e \'s/^.*Value of match was: //p\' 1>&2'
        score = subprocess.Popen(cmd2 % (wav_in, wav_out), shell=True, stderr=subprocess.PIPE)
        time.sleep(0.1)
        if score < 0.7:
            cmd3 = 'mv output.wav output_%s.wav'
            subprocess.Popen(cmd3 % score, shell=True, stderr=subprocess.PIPE)
        return 1 - float(score.stderr.readline())
    except:
        cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s %s 1>&2'
        subprocess.Popen(cmd % (midi, wav_out, plugin, vst_params), shell=True, stderr=subprocess.PIPE)
        time.sleep(0.2)
        # cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/waveform-compare %s %s | sed -n -e \'s/^.*Value in block: //p\' 1>&2'
        cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/overlap-analysis %s %s | sed -n -e \'s/^.*Value of match was: //p\' 1>&2'
        score = subprocess.Popen(cmd2 % (wav_in, wav_out), shell=True, stderr=subprocess.PIPE)
        time.sleep(0.2)
        if score < 0.7:
            cmd3 = 'mv output.wav output_%s.wav'
            subprocess.Popen(cmd3 % score, shell=True, stderr=subprocess.PIPE)
        return 1 - float(score.stderr.readline())

"""
try this:
sp = subprocess.Popen([executable, arg1, arg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = sp.communicate()
if out:
    print "standard output of subprocess:"
    print out
if err:
    print "standard error of subprocess:"
    print err
print "returncode of subprocess:"
print sp.returncode

"""

# SET NEEDED INPUT AND OUTPUT VARIABLES
# midi = '/Users/scott.cook/PycharmProjects/MindVST/samples/midi_C4_16s_1.mid'
midi = '/Users/scott.cook/Downloads/test.mid'
plugin = 'TyrellN6'
wav_in = '/Users/scott.cook/PycharmProjects/MindVST/samples/input.wav'
wav_out = '/Users/scott.cook/PycharmProjects/MindVST/samples/output.wav'

# ENSURE ALL FILES EXISTS
files_exist(midi, wav_in, wav_out)

print "[INFO] Starting Parameter Optimization for %s..." % plugin
log = open("samples/log.txt", "w")

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

    score = run_test(params)

    print "  [INFO] SCORE: %s" % score
    print "\n"
    log.write("  [INFO] SCORE: %s\n" % score)

    return score

#Import Params File
reader = csv.reader(open('main/tyrell/vst_params/TyrellN6_params.csv'))

# build vst param dictionary
vst_params = {}
row_num = 0
for row in reader:
    key = row_num
    vst_params[key] = row[0:]
    row_num += 1

def run_test(params):

    vst_params_append = ''
    for i in xrange(len(params)):
        # this prints the parameter number from Spire-1.1_params_subset.csv and then param value from the space variable
        # note that the params csv must equal the space in order for hyperopt to choose corresponding param values
        vst_params_append += " --parameter %s,%s" % (vst_params[i][0], params[i])


    print("  [INFO] vst_params = %s" % vst_params_append)
    log.write("  [INFO] vst_params = %s\n" % vst_params_append)

    global midi
    global plugin
    global wav_in
    global wav_out

    score = process_vst_and_compare(midi, plugin, vst_params_append, wav_in, wav_out)

    return score

"""
space has parameters defined in three types:
"0.1" uniform distribution between 0 and 1 for "settings"
"0.01" uniform distribution between 0 and 1 for "real numbers"
"1" uniform distribution between 0 and 1 for "binary"

see: "~/vst_params/spire-1.1_space.xlsx"

"""


space = (
    hp.quniform('p0',0,1,0.1),
    hp.quniform('p1',0,1,0.1),
    hp.quniform('p2',0,1,0.1),
    hp.quniform('p3',0,1,0.1),
    hp.quniform('p4',0,1,0.1),
    hp.quniform('p5',0,1,0.1),
    hp.quniform('p6',0,1,0.1),
    hp.quniform('p7',0,1,0.1),
    hp.quniform('p8',0,1,0.1),
    hp.quniform('p9',0,1,0.1),
    hp.quniform('p10',0,1,0.1),
    hp.quniform('p11',0,1,0.1),
    hp.quniform('p12',0,1,0.1),
    hp.quniform('p13',0,1,0.1),
    hp.quniform('p14',0,1,0.1),
    hp.quniform('p15',0,1,0.1),
    hp.quniform('p16',0,1,0.1),
    hp.quniform('p17',0,1,0.1),
    hp.quniform('p18',0,1,0.1),
    hp.quniform('p19',0,1,0.1),
    hp.quniform('p20',0,1,0.1),
    hp.quniform('p21',0,1,0.1),
    hp.quniform('p22',0,1,0.1),
    hp.quniform('p23',0,1,0.1),
    hp.quniform('p24',0,1,0.1),
    hp.quniform('p25',0,1,0.1),
    hp.quniform('p26',0,1,0.1),
    hp.quniform('p27',0,1,0.1),
    hp.quniform('p28',0,1,0.1),
    hp.quniform('p29',0,1,0.1),
    hp.quniform('p30',0,1,0.1),
    hp.quniform('p31',0,1,0.1),
    hp.quniform('p32',0,1,0.1),
    hp.quniform('p33',0,1,0.1),
    hp.quniform('p34',0,1,0.1),
    hp.quniform('p35',0,1,0.1),
    hp.quniform('p36',0,1,0.1),
    hp.quniform('p37',0,1,0.1),
    hp.quniform('p38',0,1,0.1),
    hp.quniform('p39',0,1,0.1),
    hp.quniform('p40',0,1,0.1),
    hp.quniform('p41',0,1,0.1),
    hp.quniform('p42',0,1,0.1),
    hp.quniform('p43',0,1,0.1),
    hp.quniform('p44',0,1,0.1),
    hp.quniform('p45',0,1,0.1),
    hp.quniform('p46',0,1,0.1),
    hp.quniform('p47',0,1,0.1),
    hp.quniform('p48',0,1,0.1),
    hp.quniform('p49',0,1,0.1),
    hp.quniform('p50',0,1,0.1),
    hp.quniform('p51',0,1,0.1),
    hp.quniform('p52',0,1,0.1),
    hp.quniform('p53',0,1,0.1),
    hp.quniform('p54',0,1,0.1),
    hp.quniform('p55',0,1,0.1),
    hp.quniform('p56',0,1,0.1),
    hp.quniform('p57',0,1,0.1),
    hp.quniform('p58',0,1,0.1),
    hp.quniform('p59',0,1,0.1),
    hp.quniform('p60',0,1,0.1),
    hp.quniform('p61',0,1,0.1),
    hp.quniform('p62',0,1,0.1),
    hp.quniform('p63',0,1,0.1),
    hp.quniform('p64',0,1,0.1),
    hp.quniform('p65',0,1,0.1),
    hp.quniform('p66',0,1,0.1),
    hp.quniform('p67',0,1,0.1),
    hp.quniform('p68',0,1,0.1),
    hp.quniform('p69',0,1,0.1),
    hp.quniform('p70',0,1,0.1),
    hp.quniform('p71',0,1,0.1),
    hp.quniform('p72',0,1,0.1),
    hp.quniform('p73',0,1,0.1),
    hp.quniform('p74',0,1,0.1),
    hp.quniform('p75',0,1,0.1),
    hp.quniform('p76',0,1,0.1),
    hp.quniform('p77',0,1,0.1),
    hp.quniform('p78',0,1,0.1),
    hp.quniform('p79',0,1,0.1),
    hp.quniform('p80',0,1,0.1),
    hp.quniform('p81',0,1,0.1),
    hp.quniform('p82',0,1,0.1),
    hp.quniform('p83',0,1,0.1),
    hp.quniform('p84',0,1,0.1),
    hp.quniform('p85',0,1,0.1),
    hp.quniform('p86',0,1,0.1),
    hp.quniform('p87',0,1,0.1),
    hp.quniform('p88',0,1,0.1),
    hp.quniform('p89',0,1,0.1),
    hp.quniform('p90',0,1,0.1),
    hp.quniform('p91',0,1,0.1)
)


best = fmin(run_wrapper,
            space,
            algo=tpe.suggest,
            max_evals=1)

print best

log.close()


""" PLOT WAV & SPECTROGAPHS
wav_in = "/Users/scott.cook/PycharmProjects/MindVST/samples/test_runs/test_9/input.wav"
wav_out = "/Users/scott.cook/PycharmProjects/MindVST/samples/test_runs/test_9/output_0.529.wav"

sound_features.plot_full_set(wav_in, wav_out)
"""

"""
checking output:
sed -n -e 's/^.*SCORE\: //p' log.txt | xargs printf "%0.2f\n" $T | sort | uniq -c
"""