################ PARSER ################

import numexpr as ne
import numpy as np
import re

def parse_function(equation, x):
	
	equation = adjust_equation(equation)
	
	# Now I have to create function array
	func = ne.evaluate(equation)
	
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
	return x
