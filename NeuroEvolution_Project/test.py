import network.neural_network as nn

a = nn.NeuralNetwork([2, 3, 1])

print(a.run([2.5, -4.2]))
a.print_weights()