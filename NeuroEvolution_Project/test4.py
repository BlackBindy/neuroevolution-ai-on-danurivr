from genetic.genetic import GeneticAlgorithm
from file_manager import *

ga = GeneticAlgorithm(population=15, crossover_prob=0.4, generation=50, mutation_prob=0.001, total_frames=3600, network_size=[6, 6, 6, 2], use_velocity=True)
best_enemies = ga.run_all()
save("aaa.txt", best_enemies)

a = load("aaa.txt")
print(len(a))