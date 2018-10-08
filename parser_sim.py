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
	'x1' : None,
	'x2' : None,
	'x3' : None,
	'pi' : consts.pi,
	'e' : consts.e,
	'phi' : consts.golden,
	'eps_0' : consts.epsilon_0,
	'mu_0' : consts.mu_0,
	'g' : consts.G
}

def parse_function(equation):
	
	# I'll read x arrays from the dictionary
	
	#for eq in equation:
	#    equation[eq] = adjust_equation(equation[eq])
	    
    equation  = [adjust_equation(i) for i in equation]
	
	if all(v is None for v in x):
		print("Error, unable to find x array")
		return -1
	# Now I have to create function array
	for i_eq in range(len(equation)):
	    # I rename the key of the actual x in x so I'm sure that the program won't use others vars
	    const_dic['x'] = const_dic.pop('x' + str(i_eq+1))
	    func[i_eq] = ne.evaluate(equation[i_eq],const_dic)
	    const_dic['x' + str(i_eq+1)] = const_dic.pop('x')  
	    
	# So if I want to calculate just one func I don't delete the other funcs
	if len(equation) > 1:    
	    for i_dic in range(3):
	        const_dic['x' + str(i+1)] = None
	    
	
	return func
	
def adjust_equation(eq):
	#future implementations
	# Insert a product sign between a number and a variable (ax -> a*x)
	# NB: for the moment it works for ax, but not for xa)
	
	clean_eq = re.sub(r"((?:\d+)|(?:[a-zA-Z]\w*\(\w+\)))((?:[a-zA-Z]\w*)|\()", r"\1*\2", eq)
	
	return clean_eq
	
def parse_x(sampling_times, samples_num):
	# It accepts 3 sample times
	samples_num = int(samples_num)
	
	# Convert into int
	sampling_times = list(map(int, sampling_times)) 
	
	x = [np.zeros(samples_num) for i in range(len(sampling_times))]
	for i_time in sampling_times:
	    for i_num in range(samples_num):
		    x[i_num] = float(index*sampling_times[i_time])
		    
	for i in range(3):
	    const_dic['x' + str(i+1)] = x[i]
	    
	return x
