import network.neural_network as nn

# Create a new Neural Network
a = nn.NeuralNetwork([8, 8, 6, 2])

# Run the network with artificial inputs
print(a.run([2.5, -4.2, 4.1, 0.0, -1.2, -4.2, 3.1, 0.5]))

