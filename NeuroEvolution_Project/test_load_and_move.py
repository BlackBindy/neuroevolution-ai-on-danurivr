from genetic.genetic import GeneticAlgorithm
from simulator.enemy import Enemy
from file_manager import *

path = "model/001.txt"
network_size = None # The size of a neural network

# Load the saved file
result = load(path)
print(len(result)) # = number of best enemies + 1 = number of generation + 1

# Choose a generation and create an enemy
generation_num = 10 # 11th generation (just an arbitrary choice)
network_size = result[0]
vec = result[1:] # vec: the weights of the neural network

enemy = Enemy(network_size, vec=vec[generation_num])
enemy.assign_sim_info(play_area=38, stage_rad=30, bomb_area=40) # assign the info of the game (stage size, playable area...)

# Move the enemy
position1 = enemy.pos
print(position1)

bomb_list = [] # The list of the bomb exist on the game
player_pos = (0, -38) # Current position of the player
enemy.move(bomb_list, player_pos)

position2 = enemy.pos
print(position2)

