################  PARAMETERS RECOVERY ######################
###########################################################

from pylab import *
import sympy as sm # many conflicts with pylab, numpy,math,...
from scipy import signal, random
import csv
import time
#import PSD



#####----reading data------#################
def loader(name,num,delim):
	print("started")
	t,ch1,ch2,ch3,ch4=genfromtxt(name,max_rows=num,delimiter=delim,unpack='True')
	return t,ch1,ch2,ch3,ch4


def lowfilter(data,fc,fs=2.5*10**6):
	b,a=signal.butter(4, fc/(fs/2), 'low')
	out1=signal.filtfilt(b, a, data[0])
	out2=signal.filtfilt(b, a, data[1])
	out3=signal.filtfilt(b, a, data[2])
	out4=signal.filtfilt(b, a, data[3])
	return out1,out2,out3,out4


def whitenoise(data,wpow=10**(-11),fs=2.5*10**6):
	l=len(data[0])
	sig_noise=sqrt((wpow)*fs/2)
	out1=data[0]+sig_noise*random.normal(0,1,l)
	out2=data[1]+sig_noise*random.normal(0,1,l)
	out3=data[2]+sig_noise*random.normal(0,1,l)
	out4=data[3]+sig_noise*random.normal(0,1,l)
	return out1,out2,out3,out4

def downconvert(x,flo):
	ts=x[0,10]-x[0,9]
	print("tsamp is:",ts)
	n=arange(len(x[1]))
	lo=cos(2*pi*flo*x[0])
	out1=x[1]*lo
	out2=x[2]*lo
	out3=x[3]*lo
	out4=x[4]*lo
	return out1,out2,out3,out4

def downsampl(x,ns):
	out1=signal.decimate(x[0], ns)
	out2=signal.decimate(x[1], ns)
	out3=signal.decimate(x[2], ns)
	out4=signal.decimate(x[3], ns)
	out5=signal.decimate(x[4], ns)
	return out1,out2, out3,out4,out5



def tracker(data,din=1,tin=1,pin=1):
	direct_plot_mode=0
	phase_plot_mode=0
	plot_details=1
	residual_plot=1
	#noiseactive=0
	#filteractive=0

	rex,imx,rey,imy=[],[],[],[]

	rex=data[1]
	imx=data[2]
	imy=data[3]
	rey=data[4]



	########################################
	######## DSP ALGORITHM         #########
	########################################


	#### W Matrix creation ########
	#### Symbolic calculation #####

	delta, theta,phi=sm.symbols("delta theta phi", real=True)

	##### implementation of Eo= R*M*R*Ein

	R1=sm.Matrix([[sm.cos(theta),sm.sin(theta)],[-sm.sin(theta),sm.cos(theta)]])
	M=sm.Matrix([[sm.exp(sm.I*(-delta/2)),0],[0,sm.exp(sm.I*(delta/2))]])
	R2=sm.transpose(R1)
	Fib=R2*M*R1
	Ein=sm.Matrix([sm.cos(sm.pi/4)*sm.exp(sm.I*(sm.pi/2)),sm.sin(sm.pi/4)])*sm.exp(sm.I*(phi))
	Eout=Fib*Ein

	rexS=sm.simplify(sm.re(Eout[0]))
	imxS=sm.simplify(sm.im(Eout[0]))
	reyS=sm.simplify(sm.re(Eout[1]))
	imyS=sm.simplify(sm.im(Eout[1]))

	vec=sm.Matrix([[rexS,imxS,reyS,imyS]])
	var=sm.Matrix([delta,theta,phi])

	W=vec.jacobian(var)
	Prod=sm.simplify(sm.transpose(W)*W)


	Wt=sm.lambdify((delta,theta,phi),transpose(W),'numpy')
	Prodv=sm.lambdify((delta,theta,phi),Prod,'numpy')
	Fun=sm.lambdify((delta,theta,phi),sm.transpose(vec),'numpy')


	############ main loop ##############
	########### LSM algorithm ###########


	##### declaration section ###########

	#### fundamental variables ##########

	B=array([[din],[tin],[pin]]) # Beta-point
	deB=array([[0],[0],[0]]) # Beta-increment
	Yt=array([[0],[0],[0],[0]]) # 4 values of the coherent receiver
	mod=1 # module of the Y vector
	deY=array([[0],[0],[0],[0]])
	B1=[] # auxiliary list
	B2=[] # auxiliary list
	B3=[] # auxiliary list
	dell=[] #retrieved delta
	thel=[] # retrieved theta
	phil=[] # tetreived phi
	detl=[] # determinat of (tW*W)
	sigdel=[]
	sigthe=[]
	sigphi=[]

	#weighted average
	theb=array([])
	phib=array([])
	them=B[1,0]
	phim=B[2,0]
	l=20
	thew=them
	phiw=phim
	theml=[]


	def myY(t):
		a=array([[rex[t]],[imx[t]],[rey[t]],[imy[t]]])
		return a

	def modx(x):
		b=sqrt(rex[x]**2 + imx[x]**2 + rey[x]**2 + imy[x]**2)
		return b
	###################################################

	######### loop section ###############

	print ("start loop")
	t1=time.time()


	for i in range(len(rex)):



		mod= modx(i)
		deY=(myY(i)/mod)-Yt


		Wn=Wt(B[0,0],B[1,0],B[2,0])
		u=Prodv(B[0,0],B[1,0],B[2,0])
		d=linalg.det(u)
		detl.append(1/d)


		uu=inv(u)
		#sigd=sig_noise*uu[0,0]
		#sigt=sig_noise*uu[1,1]
		#sigp=sig_noise*uu[2,2]
		deB=uu.dot(Wn).dot(deY)
		deB[1]-=trunc(deB[1]/(pi))*(pi)
		B=B+deB



		B1=B[0,0]
		B2=B[1,0]
		B3=B[2,0]

		#print("the medio:",them,"thew:",thew)
		dell.append(B1)
		thel.append(B2)
		phil.append(B3)
		#sigdel.append(sigd)
		#sigthe.append(sigt)
		#sigphi.append(sigp)

		Yt=Fun(B1,B2,B3)


	print("loop finished")
	print("elapsed time: ",time.time()-t1)
	###########################################

	return array(dell),array(thel),array(phil)

########################################################################


def normalize(x1,x2,x3,x4):
# new variables are created in order to leave the input data unchanged
	l=len(x1)
	o1=o2=o3=o4=empty(l,dtype=float)
	for i in range(l):
		mod=sqrt(x1[i]**2 + x2[i]**2 + x3[i]**2 + x4[i]**2)
		o1[i]=x1[i]/mod
		o2[i]=x2[i]/mod
		o3[i]=x3[i]/mod
		o4[i]=x4[i]/mod

	return o1,o2,o3,o4
