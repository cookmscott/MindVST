__author__ = 'scott.cook'
""" THIS ATTEMPT USES **PARTIAL** FROM Spire
 >> specifically, this will only use two oscillators
 >> pulls from Spire-1.1_params_subset.csv
"""

import csv

# get csv of param info from running the following:
# /Users/scott.cook/Documents/MrsWatson/main/mrswatson -p Obxd --display-info

# file should be of format:
# param num,param name,param value
reader = csv.reader(open('/Users/scott.cook/PycharmProjects/MindVST/main/spire/vst_params/Spire-1.1_params_subset.csv'))

from hyperopt import fmin, tpe, hp, rand
import subprocess
import time
import os.path
import sys

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
        cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s %s --quiet 1>&2'
        subprocess.Popen(cmd % (midi, wav_out, plugin, vst_params), shell=True, stderr=subprocess.PIPE)
        time.sleep(0.5)
        # cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/waveform-compare %s %s | sed -n -e \'s/^.*Value in block: //p\' 1>&2'
        cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/overlap-analysis %s %s | sed -n -e \'s/^.*Value of match was: //p\' 1>&2'
        score = subprocess.Popen(cmd2 % (wav_in, wav_out), shell=True, stderr=subprocess.PIPE)
        time.sleep(0.5)
        score = float(score.stderr.readline())
        if 1 - score < 0.93:
            cmd3 = 'mv /Users/scott.cook/PycharmProjects/MindVST/samples/output.wav /Users/scott.cook/PycharmProjects/MindVST/samples/runs/output_%s.wav'
            subprocess.Popen(cmd3 % (1 - score), shell=True, stderr=subprocess.PIPE)
        return 1 - score
    except:
        return 1.0

# SET NEEDED INPUT AND OUTPUT VARIABLES
midi = '/Users/scott.cook/PycharmProjects/MindVST/samples/midi_files/midi_A2_2s.mid'
plugin = 'Spire-1.1'
wav_in = '/Users/scott.cook/PycharmProjects/MindVST/samples/cello.wav'
wav_out = '/Users/scott.cook/PycharmProjects/MindVST/samples/output.wav'

# ENSURE ALL FILES EXISTS
files_exist(midi, wav_in, wav_out)

print "[INFO] Starting Parameter Optimization for %s..." % plugin
log = open("/Users/scott.cook/PycharmProjects/MindVST/samples/log.txt", "w")

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
    hp.quniform('p0', 0, 1, 0.1),
    hp.quniform('p1', 0, 1, 0.1),
    hp.quniform('p2', 0, 1, 0.1),
    hp.quniform('p3', 0, 1, 0.1),
    hp.quniform('p4', 0, 1, 1),
    hp.quniform('p5', 0, 1, 0.1),
    hp.quniform('p6', 0, 1, 1),
    hp.quniform('p7', 0, 1, 0.1),
    hp.quniform('p8', 0, 1, 0.1),
    hp.quniform('p9', 0, 1, 0.1),
    hp.quniform('p10', 0, 1, 0.1),
    hp.quniform('p11', 0, 1, 1),
    hp.quniform('p12', 0, 1, 0.1),
    hp.quniform('p13', 0, 1, 0.1),
    hp.quniform('p14', 0, 1, 0.1),
    hp.quniform('p15', 0, 1, 0.1),
    hp.quniform('p16', 0, 1, 0.1),
    hp.quniform('p17', 0, 1, 0.1),
    hp.quniform('p18', 0, 1, 0.1),
    hp.quniform('p19', 0, 1, 0.1),
    hp.quniform('p20', 0, 1, 0.1),
    hp.quniform('p21', 0, 1, 0.1),
    hp.quniform('p22', 0, 1, 0.1),
    hp.quniform('p25', 0, 1, 0.1),
    hp.quniform('p26', 0, 1, 0.1),
    hp.quniform('p27', 0, 1, 0.1),
    hp.quniform('p28', 0, 1, 0.1),
    hp.quniform('p29', 0, 1, 0.1),
    hp.quniform('p30', 0, 1, 0.1),
    hp.quniform('p31', 0, 1, 0.1),
    hp.quniform('p32', 0, 1, 0.1),
    hp.quniform('p33', 0, 1, 0.1),
    hp.quniform('p34', 0, 1, 0.1),
    hp.quniform('p35', 0, 1, 0.1),
    hp.quniform('p36', 0, 1, 0.1),
    hp.quniform('p37', 0, 1, 0.1),
    hp.quniform('p38', 0, 1, 0.1),
    hp.quniform('p39', 0, 1, 0.1),
    hp.quniform('p40', 0, 1, 1),
    hp.quniform('p41', 0, 1, 1),
    hp.quniform('p42', 0, 1, 1),
    hp.quniform('p43', 0, 1, 0.1),
    hp.quniform('p44', 0, 1, 0.1),
    hp.quniform('p45', 0, 1, 0.1),
    hp.quniform('p46', 0, 1, 0.1),
    hp.quniform('p47', 0, 1, 0.1),
    hp.quniform('p48', 0, 1, 0.1),
    hp.quniform('p49', 0, 1, 0.1),
    hp.quniform('p50', 0, 1, 0.1),
    hp.quniform('p51', 0, 1, 0.1),
    hp.quniform('p52', 0, 1, 0.1),
    hp.quniform('p53', 0, 1, 0.1),
    hp.quniform('p54', 0, 1, 0.1),
    hp.quniform('p55', 0, 1, 0.1),
    hp.quniform('p56', 0, 1, 0.1),
    hp.quniform('p57', 0, 1, 0.1),
    hp.quniform('p58', 0, 1, 0.1),
    hp.quniform('p59', 0, 1, 1),
    hp.quniform('p60', 0, 1, 1),
    hp.quniform('p61', 0, 1, 1),
    hp.quniform('p62', 0, 1, 0.1),
    hp.quniform('p101', 0, 1, 0.1),
    hp.quniform('p102', 0, 1, 0.1),
    hp.quniform('p103', 0, 1, 0.1),
    hp.quniform('p104', 0, 1, 0.1),
    hp.quniform('p105', 0, 1, 0.1),
    hp.quniform('p106', 0, 1, 0.1),
    hp.quniform('p107', 0, 1, 0.1),
    hp.quniform('p108', 0, 1, 0.1),
    hp.quniform('p109', 0, 1, 0.1),
    hp.quniform('p110', 0, 1, 1),
    hp.quniform('p111', 0, 1, 0.1),
    hp.quniform('p112', 0, 1, 0.1),
    hp.quniform('p113', 0, 1, 0.1),
    hp.quniform('p114', 0, 1, 0.1),
    hp.quniform('p115', 0, 1, 0.1),
    hp.quniform('p116', 0, 1, 0.1),
    hp.quniform('p117', 0, 1, 0.1),
    hp.quniform('p118', 0, 1, 0.1),
    hp.quniform('p119', 0, 1, 0.1),
    hp.quniform('p120', 0, 1, 0.1),
    hp.quniform('p121', 0, 1, 0.1),
    hp.quniform('p122', 0, 1, 0.1),
    hp.quniform('p123', 0, 1, 0.1),
    hp.quniform('p124', 0, 1, 0.1),
    hp.quniform('p125', 0, 1, 0.1),
    hp.quniform('p126', 0, 1, 0.1),
    hp.quniform('p127', 0, 1, 0.1),
    hp.quniform('p128', 0, 1, 0.1),
    hp.quniform('p129', 0, 1, 0.1),
    hp.quniform('p130', 0, 1, 0.1),
    hp.quniform('p131', 0, 1, 0.1),
    hp.quniform('p132', 0, 1, 0.1),
    hp.quniform('p133', 0, 1, 0.1),
    hp.quniform('p134', 0, 1, 0.1),
    hp.quniform('p135', 0, 1, 0.1),
    hp.quniform('p136', 0, 1, 0.1),
    hp.quniform('p137', 0, 1, 0.1),
    hp.quniform('p138', 0, 1, 0.1),
    hp.quniform('p139', 0, 1, 0.1),
    hp.quniform('p140', 0, 1, 0.1),
    hp.quniform('p141', 0, 1, 0.1),
    hp.quniform('p142', 0, 1, 0.1),
    hp.quniform('p143', 0, 1, 0.1),
    hp.quniform('p144', 0, 1, 0.1),
    hp.quniform('p145', 0, 1, 0.1),
    hp.quniform('p177', 0, 1, 0.1),
    hp.quniform('p178', 0, 1, 0.1),
    hp.quniform('p179', 0, 1, 0.1),
    hp.quniform('p180', 0, 1, 1),
    hp.quniform('p181', 0, 1, 1),
    hp.quniform('p182', 0, 1, 0.1),
    hp.quniform('p183', 0, 1, 0.1),
    hp.quniform('p184', 0, 1, 0.1),
    hp.quniform('p185', 0, 1, 0.1),
    hp.quniform('p186', 0, 1, 0.1),
    hp.quniform('p187', 0, 1, 0.1),
    hp.quniform('p188', 0, 1, 0.1),
    hp.quniform('p189', 0, 1, 0.1),
    hp.quniform('p190', 0, 1, 0.1),
    hp.quniform('p191', 0, 1, 0.1),
    hp.quniform('p192', 0, 1, 0.1),
    hp.quniform('p193', 0, 1, 0.1),
    hp.quniform('p194', 0, 1, 0.1),
    hp.quniform('p195', 0, 1, 0.1),
    hp.quniform('p196', 0, 1, 1),
    hp.quniform('p197', 0, 1, 1),
    hp.quniform('p198', 0, 1, 0.1),
    hp.quniform('p199', 0, 1, 0.1),
    hp.quniform('p200', 0, 1, 0.1),
    hp.quniform('p201', 0, 1, 0.1),
    hp.quniform('p202', 0, 1, 0.1),
    hp.quniform('p203', 0, 1, 0.1),
    hp.quniform('p204', 0, 1, 0.1),
    hp.quniform('p205', 0, 1, 0.1),
    hp.quniform('p206', 0, 1, 0.1),
    hp.quniform('p207', 0, 1, 0.1),
    hp.quniform('p208', 0, 1, 0.1),
    hp.quniform('p241', 0, 1, 0.1),
    hp.quniform('p242', 0, 1, 1),
    hp.quniform('p243', 0, 1, 0.1),
    hp.quniform('p244', 0, 1, 0.1),
    hp.quniform('p245', 0, 1, 0.1),
    hp.quniform('p246', 0, 1, 0.1),
    hp.quniform('p247', 0, 1, 0.1),
    hp.quniform('p248', 0, 1, 0.1),
    hp.quniform('p249', 0, 1, 1),
    hp.quniform('p250', 0, 1, 0.1),
    hp.quniform('p251', 0, 1, 0.1),
    hp.quniform('p252', 0, 1, 0.1),
    hp.quniform('p253', 0, 1, 0.1),
    hp.quniform('p254', 0, 1, 0.1),
    hp.quniform('p255', 0, 1, 0.1),
    hp.quniform('p256', 0, 1, 0.1),
    hp.quniform('p257', 0, 1, 1),
    hp.quniform('p258', 0, 1, 0.1),
    hp.quniform('p259', 0, 1, 0.1),
    hp.quniform('p260', 0, 1, 0.1),
    hp.quniform('p261', 0, 1, 0.1),
    hp.quniform('p262', 0, 1, 0.1),
    hp.quniform('p263', 0, 1, 0.1),
    hp.quniform('p264', 0, 1, 0.1),
    hp.quniform('p265', 0, 1, 0.1)
)

# testing with smaller space
# this list must match reader = csv.reader(open('vst_params/Spire-1.1_params_subset.csv'))
space_fine_resolution = (
    hp.quniform('p0', 0, 1, 0.1),
    hp.quniform('p1', 0, 1, 0.01),
    hp.quniform('p2', 0, 1, 0.01),
    hp.quniform('p3', 0, 1, 0.01),
    hp.quniform('p4', 0, 1, 1),
    hp.quniform('p5', 0, 1, 0.01),
    hp.quniform('p6', 0, 1, 1),
    hp.quniform('p7', 0, 1, 0.01),
    hp.quniform('p8', 0, 1, 0.01),
    hp.quniform('p9', 0, 1, 0.01),
    hp.quniform('p10', 0, 1, 0.1),
    hp.quniform('p11', 0, 1, 1),
    hp.quniform('p12', 0, 1, 0.01),
    hp.quniform('p13', 0, 1, 0.01),
    hp.quniform('p14', 0, 1, 0.01),
    hp.quniform('p15', 0, 1, 0.01),
    hp.quniform('p16', 0, 1, 0.01),
    hp.quniform('p17', 0, 1, 0.01),
    hp.quniform('p18', 0, 1, 0.01),
    hp.quniform('p19', 0, 1, 0.01),
    hp.quniform('p20', 0, 1, 0.01),
    hp.quniform('p21', 0, 1, 0.01),
    hp.quniform('p22', 0, 1, 0.01),
    hp.quniform('p25', 0, 1, 0.1),
    hp.quniform('p26', 0, 1, 0.01),
    hp.quniform('p27', 0, 1, 0.1),
    hp.quniform('p28', 0, 1, 0.01),
    hp.quniform('p29', 0, 1, 0.01),
    hp.quniform('p30', 0, 1, 0.01),
    hp.quniform('p31', 0, 1, 0.01),
    hp.quniform('p32', 0, 1, 0.1),
    hp.quniform('p33', 0, 1, 0.01),
    hp.quniform('p34', 0, 1, 0.01),
    hp.quniform('p35', 0, 1, 0.01),
    hp.quniform('p36', 0, 1, 0.1),
    hp.quniform('p37', 0, 1, 0.1),
    hp.quniform('p38', 0, 1, 0.01),
    hp.quniform('p39', 0, 1, 0.01),
    hp.quniform('p40', 0, 1, 1),
    hp.quniform('p41', 0, 1, 1),
    hp.quniform('p42', 0, 1, 1),
    hp.quniform('p43', 0, 1, 0.01),
    hp.quniform('p44', 0, 1, 0.1),
    hp.quniform('p45', 0, 1, 0.01),
    hp.quniform('p46', 0, 1, 0.01),
    hp.quniform('p47', 0, 1, 0.01),
    hp.quniform('p48', 0, 1, 0.01),
    hp.quniform('p49', 0, 1, 0.01),
    hp.quniform('p50', 0, 1, 0.01),
    hp.quniform('p51', 0, 1, 0.1),
    hp.quniform('p52', 0, 1, 0.01),
    hp.quniform('p53', 0, 1, 0.01),
    hp.quniform('p54', 0, 1, 0.01),
    hp.quniform('p55', 0, 1, 0.1),
    hp.quniform('p56', 0, 1, 0.1),
    hp.quniform('p57', 0, 1, 0.01),
    hp.quniform('p58', 0, 1, 0.01),
    hp.quniform('p59', 0, 1, 1),
    hp.quniform('p60', 0, 1, 1),
    hp.quniform('p61', 0, 1, 1),
    hp.quniform('p62', 0, 1, 0.01),
    hp.quniform('p101', 0, 1, 0.1),
    hp.quniform('p102', 0, 1, 0.1),
    hp.quniform('p103', 0, 1, 0.01),
    hp.quniform('p104', 0, 1, 0.01),
    hp.quniform('p105', 0, 1, 0.1),
    hp.quniform('p106', 0, 1, 0.1),
    hp.quniform('p107', 0, 1, 0.01),
    hp.quniform('p108', 0, 1, 0.01),
    hp.quniform('p109', 0, 1, 0.1),
    hp.quniform('p110', 0, 1, 1),
    hp.quniform('p111', 0, 1, 0.01),
    hp.quniform('p112', 0, 1, 0.01),
    hp.quniform('p113', 0, 1, 0.01),
    hp.quniform('p114', 0, 1, 0.01),
    hp.quniform('p115', 0, 1, 0.01),
    hp.quniform('p116', 0, 1, 0.01),
    hp.quniform('p117', 0, 1, 0.01),
    hp.quniform('p118', 0, 1, 0.01),
    hp.quniform('p119', 0, 1, 0.1),
    hp.quniform('p120', 0, 1, 0.1),
    hp.quniform('p121', 0, 1, 0.1),
    hp.quniform('p122', 0, 1, 0.1),
    hp.quniform('p123', 0, 1, 0.1),
    hp.quniform('p124', 0, 1, 0.01),
    hp.quniform('p125', 0, 1, 0.01),
    hp.quniform('p126', 0, 1, 0.1),
    hp.quniform('p127', 0, 1, 0.01),
    hp.quniform('p128', 0, 1, 0.01),
    hp.quniform('p129', 0, 1, 0.01),
    hp.quniform('p130', 0, 1, 0.01),
    hp.quniform('p131', 0, 1, 0.01),
    hp.quniform('p132', 0, 1, 0.01),
    hp.quniform('p133', 0, 1, 0.01),
    hp.quniform('p134', 0, 1, 0.01),
    hp.quniform('p135', 0, 1, 0.1),
    hp.quniform('p136', 0, 1, 0.1),
    hp.quniform('p137', 0, 1, 0.1),
    hp.quniform('p138', 0, 1, 0.1),
    hp.quniform('p139', 0, 1, 0.1),
    hp.quniform('p140', 0, 1, 0.01),
    hp.quniform('p141', 0, 1, 0.01),
    hp.quniform('p142', 0, 1, 0.1),
    hp.quniform('p143', 0, 1, 0.01),
    hp.quniform('p144', 0, 1, 0.01),
    hp.quniform('p145', 0, 1, 0.01),
    hp.quniform('p177', 0, 1, 0.01),
    hp.quniform('p178', 0, 1, 0.1),
    hp.quniform('p179', 0, 1, 0.01),
    hp.quniform('p180', 0, 1, 1),
    hp.quniform('p181', 0, 1, 1),
    hp.quniform('p182', 0, 1, 0.01),
    hp.quniform('p183', 0, 1, 0.01),
    hp.quniform('p184', 0, 1, 0.1),
    hp.quniform('p185', 0, 1, 0.01),
    hp.quniform('p186', 0, 1, 0.01),
    hp.quniform('p187', 0, 1, 0.1),
    hp.quniform('p188', 0, 1, 0.01),
    hp.quniform('p189', 0, 1, 0.01),
    hp.quniform('p190', 0, 1, 0.1),
    hp.quniform('p191', 0, 1, 0.01),
    hp.quniform('p192', 0, 1, 0.01),
    hp.quniform('p193', 0, 1, 0.01),
    hp.quniform('p194', 0, 1, 0.1),
    hp.quniform('p195', 0, 1, 0.01),
    hp.quniform('p196', 0, 1, 1),
    hp.quniform('p197', 0, 1, 1),
    hp.quniform('p198', 0, 1, 0.01),
    hp.quniform('p199', 0, 1, 0.01),
    hp.quniform('p200', 0, 1, 0.1),
    hp.quniform('p201', 0, 1, 0.01),
    hp.quniform('p202', 0, 1, 0.01),
    hp.quniform('p203', 0, 1, 0.1),
    hp.quniform('p204', 0, 1, 0.01),
    hp.quniform('p205', 0, 1, 0.01),
    hp.quniform('p206', 0, 1, 0.1),
    hp.quniform('p207', 0, 1, 0.01),
    hp.quniform('p208', 0, 1, 0.01),
    hp.quniform('p241', 0, 1, 0.1),
    hp.quniform('p242', 0, 1, 1),
    hp.quniform('p243', 0, 1, 0.01),
    hp.quniform('p244', 0, 1, 0.01),
    hp.quniform('p245', 0, 1, 0.01),
    hp.quniform('p246', 0, 1, 0.01),
    hp.quniform('p247', 0, 1, 0.01),
    hp.quniform('p248', 0, 1, 0.01),
    hp.quniform('p249', 0, 1, 1),
    hp.quniform('p250', 0, 1, 0.1),
    hp.quniform('p251', 0, 1, 0.01),
    hp.quniform('p252', 0, 1, 0.01),
    hp.quniform('p253', 0, 1, 0.01),
    hp.quniform('p254', 0, 1, 0.01),
    hp.quniform('p255', 0, 1, 0.01),
    hp.quniform('p256', 0, 1, 0.01),
    hp.quniform('p257', 0, 1, 1),
    hp.quniform('p258', 0, 1, 0.01),
    hp.quniform('p259', 0, 1, 0.01),
    hp.quniform('p260', 0, 1, 0.01),
    hp.quniform('p261', 0, 1, 0.01),
    hp.quniform('p262', 0, 1, 0.01),
    hp.quniform('p263', 0, 1, 0.01),
    hp.quniform('p264', 0, 1, 0.01),
    hp.quniform('p265', 0, 1, 0.01)
)

best = fmin(run_wrapper,
            space,
            algo=tpe.suggest,
            max_evals=500)

print best

log.close()

"""
checking output:
sed -n -e 's/^.*SCORE\: //p' log.txt | xargs printf "%0.2f\n" $T | sort | uniq -c
"""