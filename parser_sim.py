################ PARSER ################

import numexpr as ne
import numpy as np
import re

def parse_entry(eq_list, sampling_time, samples_num):
	
	eq_list = adjust_equation(eq_list)
	samples_num = int(samples_num)
	sampling_time = float(sampling_time)
	# Create x array 
	#x = np.arange(0,samples_num, sampling_time)
	x = np.zeros(samples_num)
	for index in range(samples_num):
		x[index] = float(index*sampling_time)
	np.set_printoptions(threshold=np.nan)
	print("x[]: ")
	print(x)
	print("sampling_times: ")
	print(sampling_time)
	print("samples_num: ")
	print(samples_num)
	
	# Now I have to create function array
	func = ne.evaluate(eq_list)
	print("values:")
	print(func)
	
def adjust_equation(eq):
	#future implementations
	# Insert a product sign between a number and a variable (ax -> a*x)
	# NB: for the moment it works for ax, but not for xa)
	
	clean_eq = re.sub(r"((?:\d+)|(?:[a-zA-Z]\w*\(\w+\)))((?:[a-zA-Z]\w*)|\()", r"\1*\2", eq)
	
	return clean_eq
	
