####################################################
##############  PSD calculation  ###################
####################################################

from pylab import *
from scipy import signal



def plotpsd(Sin,fs):


	mirroring=0

	S=Sin
	Fs=fs
	N=len(S)

	if mirroring:
		S=pad(S,(0,len(S)),'symmetric')

	S=signal.detrend(S,type='linear')
	Ys = fft(S,int(N)) #length is half of data-length
	Ysmod=2*((abs(Ys)**2)/(Fs*N**1))
	fvec=(arange(len(S)))*(Fs/len(S))
	#ax2.plot(fvec[0:int(N/2)],(Ysmod)[0:int(N/2)])
	#xax=ax2.get_xaxis().get_major_formatter()
	#xax.set_powerlimits((1,6))
	#xax.set_scientific(True)
	#ax2.grid(linestyle="--")
	#####IMPORTANT: f=0 must be omitted in PSD ##########
	#print(mean(Ysmod[1:int(N/2)]))
	#ax2.semilogy()
	#ax2.loglog()
	return fvec[1:int(N/2)],(Ysmod)[1:int(N/2)]
