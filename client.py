import numpy as np
import time

# import matplotlib.pyplot as plt

from audiostream import Audio
from fft import Fft
# from beatdetection import BeatDetect
import socket

class UdpClient():

    '''
    initialise with your ip 
    start udp on incoming port and listen for messages

    if not connected, wait for message 'Start'

        when received start sending fft over udp
        [63, 160, 400, 1000, 2500, 6250, 16000]

    else read audio

    '''

    def __init__(self, udp_ip='localhost', udp_port_rec=10000, udp_port_send=10001):

        self.ip = udp_ip
        self.port_r = udp_port_rec
        self.port_s = udp_port_send
        self.connected = False
        


    def connect(self, timeout=10):
        start_time = time.time()


        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.ip, self.port_r))


        while not self.connected:
            print 'waiting for server to connect...'
            self.__listen_for_start()
            time.sleep(0.1)
            if (time.time() - start_time) > timeout:
                print 'failed to connect before timeout'
                return False
        return True

    def __listen_for_start(self):

        data, server = self.sock.recvfrom(1024)
        print server, data

        if len(data) > 0:
            
            ''' compare data message '''
            if(data == 'Start'):
                print 'connected'
                self.connected = True
            return True
        else:
            print 'empty packet received'
            return False


    def send(self, msg):

        result = self.sock.sendto(msg, (self.ip, self.port_s))
        if result < len(msg):
            print 'not all bytes sent'
            self.connected = True
            return False
        else:
            return True

if __name__ == '__main__':
    
    '''
        CLIENT
    1 - get from source mic / wave 
    2 - apply fft
    3 - send out udp

        SERVER
    - normalise & gain [in: gain value]
    - beat detect [in: parameters]
    - send on queue
    '''

    print 'create client'
    client = UdpClient(udp_ip='localhost', udp_port_rec=10000, udp_port_send=10001)


    client.connect()

    if client.connected:

        print 'client connected'

        ''' 1 - get source '''
        datasize = 2048
        frate = 44100

        mode = 'mic'
        if mode == 'wav':
            audio = Audio(source={'input':'wav','path':'resources/DaftPunk.wav','datasize':datasize},
                    output=True)
        if mode == 'mic':
            audio = Audio(source={'input':'mic','datasize':datasize, 'rate':frate},
                    output=False)

        ''' create fft '''
        fft = Fft(datasize=datasize,frate=frate, gain=10e-4, saturation_point=1024)
        data = audio.sample_and_send()
        fft.configure_fft(data)
        fft.getDominantF()
        fft.splitLevels()     
        fft.normalize_bin_values()

        while True:
            data = audio.sample_and_send()
            fft.run_fft(data)
            fft.getDominantF()
            fft.splitLevels()     
            # fft.set_freq_bins_max()
            fft.normalize_bin_values()

            msg = ','.join([str(i) for i in fft.stats['bin_values_normalized']])
            print msg
            client.send(msg)

    else:
        print 'client not connected'

    exit()

