class Network_layer :
	def __init__(self, number_of_neurons, type_of_neurons, nodes_before, output = False):
		weights = []
		self._neurons = []
		if type_of_neurons != "input":
			nodes_before += 1 #because of bias	
			for weight in range(nodes_before):
				weights.append(1)
			for neuron in range(number_of_neurons):
				self._neurons.append(Neuron (type_of_neurons, nodes_before, weights))
		else:
			for weight in range(nodes_before):
				weights.append(0)
			for neuron in range(number_of_neurons):
				weights[neuron] = 1
				self._neurons.append(Neuron (type_of_neurons, nodes_before, weights))
				weights[neuron] = 0
		self._nodes_before = nodes_before
		self._type = type_of_neurons

	def run (self, inputs):
		if self._type != "input":		
			inputs.append(1)
		if len(inputs) != self._nodes_before:
			raise Exception("Error 1: There should be the same number of inputs as nodes before")
		outputs = []
		for neuron in self._neurons:
			outputs.append(neuron.run(inputs))
		return outputs
	
	def set_weights_manually (self, weights):
		if len(weights) != len(self._neurons):
			print (weights)
			raise Exception("Error 2: There should be the same number of weight groups as nodes in layer")
		for neuron in range(len(self._neurons)):
			self._neurons[neuron].set_weights_manually(weights[neuron])

	def __str__ (self):
		string = ""
		string += self._type
		string += " Network Layer \n"
		string += "Neurons in layer: \n"
		for neuron in self._neurons:
			string += str(neuron) 
			string += "\n"
		return string
			
				

class Neuron : 
	def __init__(self, neuron_type, nodes_before, weights, output = False):		
		if len(weights) != nodes_before:
			raise Exception("Error 3: There should be a weight for each previous node")
		self._weights = []
		self._neuron_type = neuron_type
		self._nodes_before = nodes_before
		for weight in range(nodes_before):
			self._weights.append(weights[weight])
		if neuron_type == "activation":
			self._threshold = 0

	def run(self, inputs):
		weighted_inputs = list(inputs)
		for input_index in range(len(inputs)):
			weighted_inputs[input_index] *= self._weights[input_index]
			if self._neuron_type == "input" and self._weights[input_index] == 1:
				return weighted_inputs[input_index]				
		if self._neuron_type == "activation":
			activation = sum(weighted_inputs)
			if activation >= self._threshold:
				return 1
			else:
				return 0
	
	def set_weights_manually (self, weights):
		if len(weights) != self._nodes_before:
			print (weights)
			print (self._nodes_before)
			print (self._weights)
			raise Exception( "Error 4 :There should be the same number of weights in each group as nodes in layer before" )
		self._weights = weights
		
	def __str__ (self):
		string = ""
		string += self._neuron_type
		string += " Neuron with weights: "
		string += str(self._weights)
		return string 


class Network : 
	def __init__(self, hidden_layer_node_count, input_count, output_count, neuron_type = "activation", hidden_layer_count = 1):
		self._input_layer = Network_layer(input_count, "input", input_count)
		self._hidden_layers = []		
		nodes_before = input_count
		for hidden_layer in range(hidden_layer_count):
			self._hidden_layers.append(Network_layer(hidden_layer_node_count, neuron_type, nodes_before))
			nodes_before = hidden_layer_node_count
		self._output_layer = Network_layer(output_count, "activation", nodes_before, output = True)

	def run(self, inputs):
		inputs = self._input_layer.run(inputs)
		print("\n-------------------------------------------------------------")
		print "Running neural network on input",inputs
		print("-------------------------------------------------------------")
		hidden_layer_count = 1
		for hidden_layer in self._hidden_layers:
			inputs = hidden_layer.run(inputs)
			print "After hidden layer", hidden_layer_count, "the output for the next layer is",inputs
		inputs = self._output_layer.run(inputs)
		return inputs

	def set_weights_manually(self, weights):
		if len(weights)!=len(self._hidden_layers)+1:
			print (len(self._hidden_layers))
			raise Exception( "Error 5: There should be the same number of groups of weights for layers as layers")
		for weight_layer in range(len(weights)-1):
			self._hidden_layers[weight_layer].set_weights_manually(weights[weight_layer])
		self._output_layer.set_weights_manually(weights[-1])
	
	def __str__(self):
		string = "\nNeural Network with "
		string += str(len(self._hidden_layers))
		string += " hidden layers, as well as an input and an output layer \n"
		string += "------------------------------------------------------------------------ \n"
		string += str(self._input_layer)
		string += "\n"
		for hidden_layer in self._hidden_layers:
			string += "------------------------------------------------------------------------ \n"
			string += str(hidden_layer)
			string += "\n"
		string += "------------------------------------------------------------------------ \n"
		string += str(self._output_layer)
		string += "\n"
		string += "------------------------------------------------------------------------ \n"
		string += "\n"
		return string
			

network = Network (2,2,1)
network.set_weights_manually([[[1,1,-1.5],[1,1,-0.5]],[[1,-1,0.5]]])
print(network)
print(network.run([0,0]))
print(network.run([0,1]))
print(network.run([1,0]))
print(network.run([1,1]))

  	
		
