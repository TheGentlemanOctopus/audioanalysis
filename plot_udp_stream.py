import numpy as np
import time
import socket
import matplotlib.pyplot as plt

from audiostream import Audio
from fft import Fft
from beatdetection import BeatDetect

UDP_IP = 'localhost'
UDP_PORT = 10001


if __name__ == '__main__':

    udp_ip = 'localhost'
    udp_port_rec = 10001
    udp_port_send = 10000



    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.bind((udp_ip, udp_port_rec))


    time.sleep(5)
    result = sock.sendto('Start',(UDP_IP,10000))


    history_length = 30
    bin_history = [[] for x in xrange(7)]    
    
    beat_detectors = [BeatDetect(wait=0.3, threshold=2, history=history_length) for x in xrange(7)]

    datasize = 2048
    frate = 44100

    mode = 'mic'

    if mode == 'wav':
        audio = Audio(source={'input':'wav','path':'resources/DaftPunk.wav','datasize':datasize},
                output=True)

    if mode == 'mic':
        audio = Audio(source={'input':'mic','datasize':datasize, 'rate':frate},
                output=False)



    # bin_history.append(fft.stats['bin_values_normalized'][chan])

    
    ''' populate history '''
    while (len(bin_history[0]) < history_length):
        ''' get data '''
        mStr, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = [int(e) if e.isdigit() else e for e in mStr.split(',')]
        print "received message:", data, len(data), type(data)

        for x in xrange(7):
            bin_history[x].append(data[x])



    xAxis = [x for x in xrange(history_length)]

    # plt.xlim((0, history_length))
    # plt.ylim((-0.1, 1024.1))

    animated_plots = []

    labels = ['63 Hz', '160 Hz', '400 Hz', '1 KHz', '2.5 KHz', '6.25 KHz', '16 Khz']

    print bin_history

    # for x in xrange(7):
    #     animated_plots.append(plt.plot(xAxis,bin_history[x], '-', label=labels[x], marker='o', markersize=12, markevery=[])[0])

    # plt.legend(loc='upper left')

    while True:

        ''' get data '''
        mStr, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = [int(e) if e.isdigit() else e for e in mStr.split(',')]
        
        print "received message:", data, len(data), type(data)

        for x in xrange(7):
            bin_history[x].pop(0)
            bin_history[x].append(data[x])
            beat_detectors[x].detect((bin_history[x][:]))

        
        # for x in xrange(7):
        #     animated_plots[x].set_ydata(bin_history[x])

        #     animated_plots[x].set_markevery(beat_detectors[x].history)
                        
        # plt.draw()
        # plt.pause(0.00001)

    exit()

