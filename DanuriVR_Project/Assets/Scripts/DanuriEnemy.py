import math
import Math3d
import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from genetic.genetic import GeneticAlgorithm
from simulator.enemy import Enemy
from file_manager import *

class DanuriEnemy(Actor.Actor):
	def __init__(self):
		self.danuri_enemy = Container(0)
		self.danuri_palyer = Container(0)
		self.generation_num = 0
		self.file_name = ""
		self._pos = Math3d.Vector3(0)


	def OnCreate(self, uid):
		self._pos.y = self.danuri_enemy.FindComponentByType("TransformGroup").GetPosition().y

		path = EngineFileTool.GetProjectPath() + "/Assets/Scripts" + "/model/" + self.file_name + ".txt"
		network_size = [6, 6, 6, 2] # The size of a neural network

		# Load the saved file
		best_enemies_loaded = load(path)
		print(len(best_enemies_loaded)) # = number of best enemies = number of generation

		# Choose a generation and create an enemy
		vec = best_enemies_loaded[self.generation_num] # vec: the weights of the neural network
		self.enemy = Enemy(network_size, vec=vec)
		self.enemy.assign_sim_info(play_area=38, stage_rad=30, bomb_area=40) # assign the info of the game (stage size, playable area...)


	def Update(self):
		danuri_palyer_pos = self.danuri_palyer.FindComponentByType("TransformGroup").GetPosition()
		danuri_palyer_pos = (danuri_palyer_pos.x, danuri_palyer_pos.z)
		#print(danuri_palyer_pos)
		self.move(danuri_palyer_pos)


	def move(self, player_pos):
		bomb_list = [] # The list of the bomb exist on the game
		self.enemy.move(bomb_list, player_pos)

		# move danuri enemy
		self._pos.x = self.enemy.pos[0]
		self._pos.z = self.enemy.pos[1]
		self.danuri_enemy.FindComponentByType("TransformGroup").SetPosition(self._pos)