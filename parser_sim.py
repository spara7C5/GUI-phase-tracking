################ PARSER ################


import numexpr as ne

def parse_entry(eq_list, samples):
	x = samples
	out_eq = []
	if eq_list == []:
		# The given is empty
		print("Parse error: The passed list is empty")
		return []
	
	for eq in eq_list:
		print("eq: " + eq)
		out_eq.append(ne.evaluate(eq_list[eq]))
	return out_eq
	
def adjust_equation(eq):
	#future implementations
	return
	
