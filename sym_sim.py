


import sympy as sm
############# explicit import to avoid conflicts with sympy ################
from numpy import pi,array,fabs,e,sin,cos,arccos,arange,linspace 
############################################################################
from matplotlib.pyplot import *

from scipy.signal import square

import mpmath as mpm

delta, theta,phi,Y1,Y2,Y3,Y4,p,E=sm.symbols("delta theta phi Y1 Y2 Y3 Y4 p E", real=True)


def round2zero(m, e):
	for i in range(m.shape[0]):
		for j in range(m.shape[1]):
			if abs(m[i,j]) < e:
				m[i,j] = 0

def myabs(x):
	return sm.sqrt((sm.re(x)**2)+(sm.im(x)**2))

###generic birefringent element
#theta=sm.pi/4
#delta=sm.pi
R1=sm.Matrix([[sm.cos(theta),sm.sin(theta)],[-sm.sin(theta),sm.cos(theta)]])
M=sm.Matrix([[sm.exp(sm.I*(-delta/2)),0],[0,sm.exp(sm.I*(delta/2))]])
R2=sm.transpose(R1)
Fib=R2*M*R1*sm.exp(sm.I*(phi))
#Fib=sm.Matrix([[0,-1],[-1,0]])

sm.pprint(Fib)


## non ideal Faraday rotator
Mag=sm.Matrix([[sm.cos(p),-sm.sin(p)],[sm.sin(p),sm.cos(p)]])
## simple mirror
Mir=sm.Matrix([[1,0],[0,1]])

Magv=sm.lambdify(p,Mag,'numpy')
#######
print("insert rotation angle:")
angs=int(input())
#######
## faraday mirror
ang=angs*(pi/180)
FM=Magv(ang)*Mir*Magv(ang)
round2zero(FM,10**(-15))
sm.pprint("FM= ")
sm.pprint(FM)
Roundtrip=Fib*FM*Fib

## Launched Field

Ein=sm.Matrix([[sm.cos(sm.pi/4)*sm.exp(sm.I*(sm.pi/2))],[sm.sin(sm.pi/4)]])*E##*sm.exp(sm.I*(phi))
Eout=Roundtrip*Ein

## reflection on the short branch NOTE: THIS IS CONSIDERED AS PERFECT
Einr=sm.Matrix([[666],[666]])
Einr[0,0],Einr[1,0]=-Ein[1,0],Ein[0,0]
angssh=45
angsh=angssh*(pi/180)
FMsh=Magv(angsh)*Mir*Magv(angsh)
round2zero(FMsh,10**(-15))
Einr=FMsh*Ein

beatvec=(sm.Matrix([[myabs(sm.simplify(Einr[0,0]+Eout[0,0]))],[myabs(sm.simplify(Einr[1,0]+Eout[1,0]))]]))
beat=(beatvec[0,0]**2)+(beatvec[1,0]**2)
sm.pprint("Ein= ")
sm.pprint(sm.factor(sm.simplify(Ein)))
sm.pprint("Eout= ")
sm.pprint((sm.trigsimp(Eout)))
sm.pprint("Abs(Eout+Einr)= ")
sm.pprint(beatvec)

##results:
sm.pprint(sm.simplify(beat-2*E**2)) #it deletes the constant term to visualize the only oscillating term



beatv=sm.lambdify((E,delta,theta,phi),beat-2*E**2,'numpy')


print("================================ \n================================")

dell=array([0 for x in linspace(0,10,4000)])
#dell=array([0.5*x for x in linspace(0,10,4000)])+0.1*square([x for x in linspace(0,4*(2*pi),4000)])
#dell=array(([sin(x) for x in linspace(0,4*(2*pi),2000)]))

thel=array([0.5+0.5*x for x in linspace(0,10,4000)])+0.1*square([x for x in linspace(0,4*(2*pi),4000)])
#thel=array([0.3*sin(x) for x in linspace(0,2*pi,2000)])

phil=array([1 for x in linspace(0,10,4000)])
#phil=array(0.1*square([x for x in linspace(0,4*(2*pi),2000)]))
#phil=array([1 for x in linspace(0,1,2000)])

detval=beatv(1,dell,thel,phil)
detphase=(arccos(detval/2))/2 #from the interference formula
#print(detphase)


f1=figure()
s1=f1.add_subplot(111)
s1.plot(detphase,"blue",label="far.rotat.={}".format(angs))
s1.plot(dell,"red",label="delta")
s1.plot(thel,"orange",label="theta")
s1.plot(phil,"green",label="isotr. phi shift")
s1.plot(phil-detphase,"purple",label="phase diff")
s1.set_ylabel("phase/angle (rad)")
s1.grid()
s1.legend()
show()



'''

rexS=sm.simplify(sm.re(Eout[0,0]))
imxS=sm.simplify(sm.im(Eout[0,0]))
reyS=sm.simplify(sm.re(Eout[1,0]))
imyS=sm.simplify(sm.im(Eout[1,0]))

vec=sm.Matrix([[rexS,imxS,reyS,imyS]])
var=sm.Matrix([delta,theta,phi])

W=sm.simplify(vec.jacobian(var))
Prod=sm.simplify(sm.transpose(W)*W)


Wt=sm.lambdify((delta,theta,phi),sm.transpose(W),'numpy')
Prodv=sm.lambdify((delta,theta,phi),Prod,'numpy')
Fun=sm.lambdify((delta,theta,phi),sm.transpose(vec),'numpy')

Y=sm.Matrix([[Y1],[Y2],[Y3],[Y4]])
#sm.pprint(u)
#uu=inv(u)
#deB=uu.dot(Wt).dot(Y)

#sm.pprint(Y)

p1=(sm.transpose(W)*Y)
p2=(Prod.inv())

#sm.pprint(sm.simplify(p2*p1))


deltas=((Prod.inv())*sm.transpose(W)*Y)

##sm.pprint(((sm.simplify(sm.trigsimp(sm.factor(deltas[1]))))))

sm.pprint(((sm.factor(sm.trigsimp(sm.simplify(deltas[1]))))))



#sm.pprint(sm.simplify((W)))

'''

