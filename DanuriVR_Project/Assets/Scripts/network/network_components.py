from . import numeric_components as num

class Dendrite:
	def __init__(self, weight=None): # Random value : [0.0, 1.0)
		if weight == None:
			self.weight = num.get_rand()
		else:
			self.weight = weight

class Neuron:
	def __init__(self, dendrite_list=[], bias=None):
		self.dendrite_list = dendrite_list
		if bias == None:
			self.bias = num.get_rand()
		else:
			self.bias = bias
		self.delta = 0
		self.value = 0

class Layer:
	def __init__(self, neuron_list=[]):
		self.neuron_list = neuron_list