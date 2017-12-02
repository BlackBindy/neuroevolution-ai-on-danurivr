from genetic.genetic import GeneticAlgorithm
from simulator.enemy import Enemy
from file_manager import *

path = "model/001.txt"
network_size = [6, 6, 6, 2] # The size of a neural network

# Run GeneticAlgorithm
ga = GeneticAlgorithm(population=15, crossover_prob=0.4, generation=50, mutation_prob=0.001, total_frames=3600, network_size=network_size, use_velocity=True)
best_enemies = ga.run_all()

# Save the best enemy of each generation
save(path, network_size, best_enemies)

# Load the saved file
best_enemies_loaded = load(path)
print(len(best_enemies_loaded)) # = number of best enemies = number of generation

# Choose a generation and make an enemy
generation_num = 10 # 11th generation
vec = best_enemies_loaded[generation_num] # vec: the weights of the neural network
enemy = Enemy(network_size, vec=vec)
enemy.assign_sim_info(play_area=38, stage_rad=30, bomb_area=40) # assign the info of the game

# Move the enemy
position1 = enemy.pos
print(position1)

bomb_list = [] # The list of the bomb exist on the game
player_pos = (0, -38) # Current position of the player
enemy.move(bomb_list, player_pos)

position2 = enemy.pos
print(position2)

