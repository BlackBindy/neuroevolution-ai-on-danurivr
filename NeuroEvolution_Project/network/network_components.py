import random as rd

class Dendrite:
	def __init__(self, init_weight=True, weight=0): # Random value : [0.0, 1.0)
		if init_weight:
			self.weight = rd.gauss(0, 1)
		else:
			self.weight = weight

class Neuron:
	def __init__(self, dendrite_list=[], init_bias=True, bias=0):
		self.dendrite_list = dendrite_list
		if init_bias:
			self.bias = rd.gauss(0, 1)
		else:
			self.bias = bias
		self.delta = 0
		self.value = 0

class Layer:
	def __init__(self, neuron_list=[]):
		self.neuron_list = neuron_list