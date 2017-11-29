from . import network_components as net
from . import numeric_components as num

class NeuralNetwork:
	def __init__(self, layout, activation='tanh', weights=None): # layout : the array of int, layout[i] indicates the number of nodes of ith layer
		if len(layout) < 2:
			raise IndexError("The length of layout [" + str(len(layout)) + "] is less than 2")

		if(activation == 'sigmoid'):
			self.activation = num.sigmoid
		elif(activation == 'tanh'):
			self.activation = num.tanh
		elif(activation == 'relu'):
			self.activation = num.relu
		else:
			raise NameError("There is no [" + activation + "] function.")

		layer_list = []

		for l in range(len(layout)):
			# Initialize a neuron_list with the length of l
			neuron_list = []
			for n in range(layout[l]): # [0, l)
				# Initialize a neuron and connect dendrites behind it
				neuron = net.Neuron()
				if l == 0:
					neuron.bias = 0
				else:
					dendrite_list = []
					for d in range(layout[l-1]):
						dendrite_list.append(net.Dendrite(init_weight=True))
					neuron.dendrite_list = dendrite_list
				neuron_list.append(neuron)

			# Initialize a layer with the neuron_list above
			layer = net.Layer(neuron_list)

			# Add the layer to layer_list
			layer_list.append(layer)
			self.layer_list = layer_list

	# The neural network runs and return the output
	def run(self, input):
		if len(input) != len(self.layer_list[0].neuron_list):
			raise BaseException("The number of input is not equal to the size of input layer")

		for l in range(len(self.layer_list)):
			layer = self.layer_list[l]
			neuron_list = layer.neuron_list

			for n in range(len(neuron_list)):
				neuron = neuron_list[n]

				if l == 0:
					neuron.value = input[n]
				else:
					value = 0		
					dendrite_list = neuron.dendrite_list	

					for d in range(len(dendrite_list)):
						dendrite = neuron.dendrite_list[d]
						value += dendrite.weight * self.layer_list[l-1].neuron_list[d].value
						
					
					value = self.activation(value + neuron.bias)
					neuron.value = value

		return [neuron.value for neuron in self.layer_list[len(self.layer_list) - 1].neuron_list]

	# Print all the weights of the network
	def print_weights(self):
		for l in range(len(self.layer_list)):
			layer = self.layer_list[l]
			neuron_list = layer.neuron_list

			result_layer = ""
			for n in range(len(neuron_list)):				
				neuron = neuron_list[n]

				result_neuron = ""
				for dendrite in neuron.dendrite_list:
					result_layer += "[" + "%.4f"%(dendrite.weight) + "] "

				result_layer += result_neuron + " / "

			if(l > 0):
				print(result_layer)

	# Vectorize the weights and the biases
	def vectorize(self):
		vec = []
		for l in range(len(self.layer_list)):
			for neuron in len(neuron_list):
				for dendrite in neuron.dendrite_list:
					vec.append(dendrite.weight)
				vec.append(neuron.bias)