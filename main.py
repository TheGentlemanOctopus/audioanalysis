import numpy as np
import time
from multiprocessing import Process, Queue

# import matplotlib.pyplot as plt

from audiostream import Audio
from fft import Fft
from client import FftClient
# from beatdetection import BeatDetect
import socket

''' this process emulates the arduino with msgeq7 chip '''

if __name__ == '__main__':

    c = FftClient(process_period=0.02,
            udp_ip='localhost', 
            udp_port_rec=10000, 
            udp_port_send=10001,
            datasize=2048,
            frate=44100,
            mode='mic')

    c.daemon = True
    c.start()

    while True:
        time.sleep(1)
        pass

