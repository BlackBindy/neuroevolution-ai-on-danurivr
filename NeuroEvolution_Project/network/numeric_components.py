import math
import random as rd

def sigmoid(x):
	return 1 / (1 + math.exp(-x))

def tanh(x):
	doubled_exp = math.exp(2 * x)
	return ((doubled_exp - 1) / (doubled_exp + 1))

def relu(x):
	if (x > 0):
		return x
	else:
		return 0

def get_rand():
	return rd.gauss(0, 1)