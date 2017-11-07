import math

def Sigmoid(x):
	return 1 / (1 + math.exp(-x))

def Tanh(x):
	doubled_exp = math.exp(2 * x)
	return ((doubled_exp - 1) / (doubled_exp + 1))