from genetic.genetic import GeneticAlgorithm
from file_manager import *

path = "model/002.txt"
network_size = [6, 6, 6, 2] # The size of a neural network

# Run GeneticAlgorithm
ga = GeneticAlgorithm(population=15, crossover_prob=0.4, generation=50, mutation_prob=0.001, total_frames=3600, network_size=network_size, use_velocity=True)
best_enemies = ga.run_all()

# Save the best enemy of each generation
save(path, best_enemies)