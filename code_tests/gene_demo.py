#! /usr/bin/env python3

"""
Very simple demo in which organisms try to minimise
the output value of a function
"""

from pygene3.gene import FloatGene, FloatGeneMax, IntGeneRandom
from pygene3.organism import Organism, MendelOrganism
from pygene3.population import Population
import subprocess
import time

def process_vst(midi, plugin, wav_out, p1, p2):
    """
    # delete file if exists
    try:
        os.remove(wav_out)
    except OSError:
        pass
    """
    cmd = '/Users/scott.cook/Documents/MrsWatson/main/mrswatson -m %s -o %s -p %s --parameter 4,%s --parameter 44,%s 1>&2'
    subprocess.Popen(cmd % (midi, wav_out, plugin, p1, p2), shell=True, stderr=subprocess.PIPE)

def waveform_compare(wav1, wav2):
    # Run waveform-compare and grab stdout
    cmd = '/Users/scott.cook/Documents/scape-xcorrsound/build/apps/overlap-analysis %s %s | sed -n -e \'s/^.*Value of match was: //p\''
    score = subprocess.Popen(cmd % (wav1, wav2), shell=True, stdout=subprocess.PIPE)
    time.sleep(0.2)
    return float(score.stdout.readline())

# SET NEEDED INPUT AND OUTPUT VARIABLES
midi = '/Users/scott.cook/Downloads/output_1.mid'
plugin = 'Obxd'
wav_in = '/Users/scott.cook/PycharmProjects/MindVST/input.wav'
wav_out = '/Users/scott.cook/PycharmProjects/MindVST/output.wav'

class CvGene(FloatGeneMax):
    """
    Gene which represents the numbers used in our organism
    """
    # genes get randomly generated within this range
    randMin = 0
    randMax = 1
    # probability of mutation
    mutProb = 0.1
    # degree of mutation
    mutAmt = 4

class Converger(MendelOrganism):
    """
    Implements the organism which tries
    to converge a function
    """
    genome = {'p1': CvGene, 'p2': CvGene}

    def fitness(self):
        """
        Implements the 'fitness function' for this species.
        Organisms try to evolve to minimise this function's value
        """
        p1 = self['p1']
        p2 = self['p2']

        # generate output.wav
        process_vst(midi, plugin, wav_out, p1, p2)

        # compare input and output wav
        # Organism tries to evolve to minimise output of difference between input and output wav files
        score = waveform_compare(wav_in, wav_out)
        print "%s, %s, %s" % (score, p1, p2)
        if score < 0.7:
            return 100 * (1 - score)
        if score > 0.7:
            return 1 - score

    def __repr__(self):
        return "<Converger fitness=%f p1=%s p2=%s>" % (
            self.fitness(), self['p1'], self['p2'])


# create an empty population

pop = Population(species=Converger, init=2, childCount=50, childCull=5)


# now a func to run the population

def main():
    try:
        while True:
            # execute a generation
            pop.gen()

            # get the fittest member
            # best = pop.best()
            best = pop.organisms[0]

            # and dump it out
            print("**FITNESS**=%f p1=%f p2=%f" % (best.get_fitness(), best['p1'], best['p2']))

            if best.get_fitness() < 0.3:
                break

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()


