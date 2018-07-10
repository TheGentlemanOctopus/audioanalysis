import matplotlib.pyplot as plt

from audiostream import Audio
from fft import Fft

if __name__ == '__main__':

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
	fft.run_fft(data)
	
	
	plt.xlim((0, 4000))
	plt.ylim((-10, 3000000))

	animated_plot = plt.plot(fft.stats['frequencies'],fft.stats['fft_out'], '-')[0]


	# plt.xlim((0, 7))
	# plt.ylim((-0.1, 1.1))

	# animated_plot = plt.plot(fft.stats['freq_bins'],fft.stats['bin_values_normalized'], '-')[0]



	print 'frequencies:', fft.freqs


	# for i in fft.freqs:
	# 	print i

	while True:
		data = audio.sample_and_send()
		fft.run_fft(data)
		fft.getDominantF()
		fft.splitLevels(fft_out)     
		fft.set_freq_bins_max()
		fft.normalize_bin_values()

		print fft.stats['bin_values_normalized']

		# print fft.freqHz

		animated_plot.set_ydata(fft.stats['fft_out'])
		# animated_plot.set_ydata(fft.stats['bin_values_normalized'])
		plt.draw()
		plt.pause(0.00001)




	exit()