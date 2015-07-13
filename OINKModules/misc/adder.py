def add(a,b):
	"""adds a and b.
	>>> add(1,0)
	1
	>>> add(1,2)
	3
	>>> add(1,-1)
	0
"""
	return a + b

if __name__ == "__main__":
	import doctest
	doctest.testmod()