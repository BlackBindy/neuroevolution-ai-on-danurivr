import network.neural_network as nn

# Create a new Neural Network
a = nn.NeuralNetwork([2, 3, 1])

# Print the current weights of the network
a.print_weights()
print()

# Run the network with artificial inputs
print(a.run([2.5, -4.2]))
print()

# Print the vectorized weights and biases of the network
a_vec = a.vectorize()
print(a_vec)
print()

# Test devectorizing
b = nn.NeuralNetwork([2, 3, 1], vec=a_vec)
b_vec = a.vectorize()
print(b_vec)
print()

# Test devectorizing - should raise error
c = nn.NeuralNetwork([4, 5, 2], vec=a_vec)

