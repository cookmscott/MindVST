import blackbox as bb
import subprocess
import time

midi = '/Users/scott.cook/PycharmProjects/MindVST/samples/midi_files/midi_As3_900ms.mid'
plugin = 'Obxd'
wav_in = '/Users/scott.cook/PycharmProjects/MindVST/samples/obxd_30sampls_a3_input.wav'
wav_out = '/Users/scott.cook/PycharmProjects/MindVST/samples/output.wav'
cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s %s 1>&2'

def fun(par):
    # vst_params = '--parameter 1,%s --parameter 2,%s --parameter 3,%s --parameter 4,%s --parameter 5,%s --parameter 6,%s --parameter 7,%s --parameter 8,%s --parameter 9,%s --parameter 10,%s --parameter 11,%s --parameter 12,%s --parameter 13,%s --parameter 14,%s --parameter 15,%s --parameter 16,%s --parameter 17,%s --parameter 18,%s --parameter 19,%s --parameter 20,%s --parameter 21,%s --parameter 22,%s --parameter 23,%s --parameter 24,%s --parameter 25,%s --parameter 26,%s --parameter 27,%s --parameter 28,%s --parameter 29,%s --parameter 30,%s' % (par[0],par[1],par[2],par[3],par[4],par[5],par[6],par[7],par[8],par[9],par[10],par[11],par[12],par[13],par[14],par[15],par[16],par[17],par[18],par[19],par[20],par[21],par[22],par[23],par[24],par[25],par[26],par[27],par[28],par[29])
    vst_params = '--parameter 1,%s --parameter 2,%s --parameter 3,%s --parameter 4,%s --parameter 5,%s --parameter 6,%s' % (par[0],par[1],par[2],par[3],par[4],par[5])
    print vst_params
    print cmd % (midi, wav_out, plugin, vst_params)
    subprocess.Popen(cmd % (midi, wav_out, plugin, vst_params), shell=True, stderr=subprocess.PIPE)
    time.sleep(0.5)
    cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/waveform-compare %s %s --pad-short-block | sed -n -e \'s/^.*Value in block: //p\' 1>&2'
    # cmd2 = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/overlap-analysis %s %s | sed -n -e \'s/^.*Value of match was: //p\' 1>&2'
    print cmd2 % (wav_out, wav_in)
    score = subprocess.Popen(cmd2 % (wav_out, wav_in), shell=True, stderr=subprocess.PIPE)
    score = float(score.stderr.readline())
    print 1 - score
    return 1 - score

def main():
    bb.search(f=fun,  # given function
              box=[[0., 1.], [0., 1.], [0., 1.], [0., 1.], [0., 1.], [0., 1.]],  # range of values for each parameter
              n=40,  # number of function calls on initial stage (global search)
              m=40,  # number of function calls on subsequent stage (local search)
              batch=1,  # number of calls that will be evaluated in parallel
              resfile='output.csv')  # text file where results will be saved


if __name__ == '__main__':
    main()