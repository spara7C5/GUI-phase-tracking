################ PARSER ################

import numexpr as ne
import numpy as np
import re
from scipy import constants as consts

# x variable is initialized to None (NoneType)
# When I call parse_x I update the value of x to the actual domain array
# After I've evaluated the function I set x again to None in order to
# remember to change the x array for the new function

const_dic = {
	'x' : None,
	'pi' : consts.pi,
	'e' : consts.e,
	'phi' : consts.golden,
	'eps_0' : consts.epsilon_0,
	'mu_0' : consts.mu_0,
	'g' : consts.G
}

def parse_function(equation):
	
	equation = adjust_equation(equation)
	
	#if None == x.any():
	#	print("Error, unable to find x array")
	#	return -1
	# Now I have to create function array
	func = ne.evaluate(equation,const_dic)
	#const_dic['x'] = None
	
	return func
	
def adjust_equation(eq):
	#future implementations
	# Insert a product sign between a number and a variable (ax -> a*x)
	# NB: for the moment it works for ax, but not for xa)
	
	clean_eq = re.sub(r"((?:\d+)|(?:[a-zA-Z]\w*\(\w+\)))((?:[a-zA-Z]\w*)|\()", r"\1*\2", eq)
	
	return clean_eq
	
def parse_x(sampling_time, samples_num):
	samples_num = int(samples_num)
	sampling_time = float(sampling_time)
	
	x = np.zeros(samples_num)
	for index in range(samples_num):
		x[index] = float(index*sampling_time)
	const_dic['x'] = x
	#return x
