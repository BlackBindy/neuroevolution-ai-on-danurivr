from . import network_components as net
from . import numeric_components as num

class NeuralNetwork:
	def __init__(self, layout, activation='tanh', vec=None): # layout : the array of int, layout[i] indicates the number of nodes of ith layer
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
		vec_index = 0

		# Check if the size of the vector is correct
		if vec != None:
			correct_num = 0
			for i in range(len(layout)):
				if i == 0:
					continue
				cur_len = layout[i]
				prv_len = layout[i-1]
				correct_num += (prv_len * cur_len) + cur_len # num of dendrites + num of biases

			if correct_num != len(vec):
				raise IndexError("The size of layout and vector are not equal")

		for l in range(len(layout)):
			# Initialize a neuron_list with the length of l
			neuron_list = []
			for n in range(layout[l]): # [0, l)				
				if vec == None: # Initalizing case					
					dendrite_list = []
					for d in range(layout[l-1]):
						dendrite_list.append(net.Dendrite())

					if l == 0:
						neuron = net.Neuron(dendrite_list=dendrite_list, bias=0)
					else:
						neuron = net.Neuron(dendrite_list=dendrite_list)
				else: # Devectorizing case					
					dendrite_list = []
					for d in range(layout[l-1]):
						if l == 0:
							dendrite_list.append(net.Dendrite())
						else:
							dendrite_list.append(net.Dendrite(weight=vec[vec_index]))
							vec_index += 1
						
					if l == 0:
						neuron = net.Neuron(dendrite_list=dendrite_list, bias=0)
					else:
						neuron = net.Neuron(dendrite_list=dendrite_list, bias=vec[vec_index])
						vec_index += 1

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
			if l == 0:
				continue
			else:
				layer = self.layer_list[l]

			for neuron in layer.neuron_list:
				for dendrite in neuron.dendrite_list:
					vec.append(dendrite.weight)
				vec.append(neuron.bias)
		return vec