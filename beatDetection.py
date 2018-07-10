import numpy as np
from peakutils.peak import indexes

import matplotlib.pyplot as plt

from audiostream import Audio
from fft import Fft


class PeakDetection():

    def __init__(self, wave):

        indexes = indexes(np.array(vector), thres=7.0/max(vector), min_dist=2)
        return indexes
        




if __name__ == '__main__':
    
    # vector = [ 0, 6, 25, 20, 15, 8, 15, 6, 0, 6, 0, -5, -15, -3, 4, 10, 8, 13, 8, 10, 3, 1, 20, 7, 3, 0 ]
    # print('Detect peaks with minimum height and distance filters.')
    # indexes = indexes(np.array(vector), thres=7.0/max(vector), min_dist=2)
    # print('Peaks are: %s' % (indexes))


    history_length = 30
    chan = 0

    bin_history = [[] for x in xrange(7)]

    # grab audio until history builds
    datasize = 2048
    frate = 44100

    mode = 'mic'

    if mode == 'wav':
        audio = Audio(source={'input':'wav','path':'resources/DaftPunk.wav','datasize':datasize},
                output=True)

    if mode == 'mic':
        audio = Audio(source={'input':'mic','datasize':datasize, 'rate':frate},
                output=False)

    fft = Fft(datasize=datasize,frate=frate)
    
    data = audio.sample_and_send()
    fft.configure_fft(data)
    fft.getDominantF()
    fft.splitLevels()     
    fft.normalize_bin_values()

    # bin_history.append(fft.stats['bin_values_normalized'][chan])

    print len(bin_history)

    while (len(bin_history[0]) < history_length):
        data = audio.sample_and_send()
        fft.configure_fft(data)
        fft.getDominantF()
        fft.splitLevels()     
        fft.normalize_bin_values()
        for x in xrange(7):
            bin_history[x].append(fft.stats['bin_values_normalized'][x])

    # plt.xlim((0, 4000))
    # plt.ylim((-10, 3000000))

    # animated_plot = plt.plot(fft.stats['frequencies'],fft.stats['fft_out'], '-')[0]

    xAxis = [x for x in xrange(history_length)]

    plt.xlim((0, history_length))
    plt.ylim((-0.1, 100.1))

    animated_plots = []

    for x in xrange(7):
            animated_plots.append(plt.plot(xAxis,bin_history[x], '-', marker='o', markersize=12, markevery=[])[0])
    

    # for i in fft.freqs:
    #   print i
    while True:
        data = audio.sample_and_send()
        fft.run_fft(data)
        fft.getDominantF()
        fft.splitLevels()     
        # fft.set_freq_bins_max()
        fft.normalize_bin_values()

        for x in xrange(7):
            bin_history[x].pop(0)
            bin_history[x].append(fft.stats['bin_values_normalized'][x])

        
        
        for x in xrange(7):
            animated_plots[x].set_ydata(bin_history[x])

            if x == chan:
                idx = indexes( np.array(bin_history[x]), thres=.8, min_dist=10)
                animated_plots[x].set_markevery(idx.tolist())
                
                
                    
        # idx = [0]

        plt.draw()
        plt.pause(0.00001)




    exit()

