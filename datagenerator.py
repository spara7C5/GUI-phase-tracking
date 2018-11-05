

### SIMULATOR OF THE OPTICAL FIBER ######


from numpy import *
import matplotlib.colors
import csv
from matplotlib.pyplot import *
matplotlib.use("TkAgg") #setting Tk ad windows manager
from mpl_toolkits.mplot3d import Axes3D
import time

###### fiber model: Jones calculation ########
def fibmod(delta,theta,phi):
	R1=array([[cos(theta),sin(theta)],[-sin(theta),cos(theta)]])
	M=array([[e**(1j*(-delta/2)),0],[0,e**(1j*(delta/2))]])
	R2=transpose(R1)
	Ein=array([cos(pi/4)*e**(1j*(pi/2)),sin(pi/4)])*e**(1j*(phi))
	return R2.dot(M.dot(R1.dot(Ein)))


##### MAIN FUNCTION TO BE IMPORTED #####################

def datagen(dearr,thearr,phiarr):


	t,rex,imx,rey,imy=[],[],[],[],[]

	for i in arange(len(dearr)):
		dd=dearr[i]
		tt=thearr[i]
		pp=phiarr[i]
		
		Eout=fibmod(dd,tt,pp)
		Exr=Eout[0].real
		Exi=Eout[0].imag
		Eyr=Eout[1].real
		Eyi=Eout[1].imag
		rex.append(Exr)
		imx.append(Exi)
		rey.append(Eyr)
		imy.append(Eyi)
		t.append(i)


	## writing ALSO on file
	outlist=list(zip(t,rex,imx,rey,imy))
	f=open("eout.csv",'w')
	w=csv.writer(f, delimiter='\t')
	w.writerows(outlist)
	f.close()

	#the order of the output is the same of the
	#experimental setup real-imag-imag-real
	return array(rex), array(imx), array(imy), array(rey)

### random walk generator ###########

import numpy.random as npr
class RandomWalk:

	def __init__(self, pow1hz,fs):
		self.last=0
		self.randlis=[]
		self.ampli=sqrt(2*pi*pi*pow1hz/fs)

	def funrand(self,t):
		for i in range(t):
			step = npr.normal(0,1)
			self.last+= step #+ (10**(-5))*npr.normal())
			self.randlis.append(self.last)
		self.randarr=array(self.randlis)
		self.randarr*=self.ampli
