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
		self.bomb_con = Container(0)
		self.generation_num = 0
		self.file_name = ""
		self._pos = Math3d.Vector3(0)
		self.enemy = None
		self.is_created = False


	def OnCreate(self, uid):
		self.bomb_con_script = self.bomb_con.FindComponentByType("ScriptComponent")
		self.bomb_con_actor = self.bomb_con_script.GetActor()

		self._init_pos = self.danuri_enemy.FindComponentByType("TransformGroup").GetPosition()
		self._pos.y = self.danuri_enemy.FindComponentByType("TransformGroup").GetPosition().y

		# Load the network
		self.load_enemies(self.file_name, self.generation_num)
		self.is_created = True

	def Update(self):
		if self.enemy == None:
			return 0
		elif self.enemy.is_dead == True:
			self.load_enemies(self.file_name, self.generation_num)
			self.change_show(1)
			return 0
			
		danuri_palyer_pos = self.danuri_palyer.FindComponentByType("TransformGroup").GetPosition()
		danuri_palyer_pos = (danuri_palyer_pos.x, danuri_palyer_pos.z)
		#print(danuri_palyer_pos)
		self.move(danuri_palyer_pos)


	def load_enemies(self, file_name, generation_num):
		self.file_name = file_name
		self.generation_num = generation_num
		path = EngineFileTool.GetProjectPath() + "/Assets/Scripts" + "/model/" + file_name + ".txt"

		# Load the saved file
		result = load(path)
		network_size = result[0]
		best_enemies = result[1:]
		print("Load enemies: ", len(best_enemies)) # = number of best enemies = number of generation

		# Choose a generation and create an enemy
		vec = best_enemies[generation_num] # vec: the weights of the neural network
		self.enemy = Enemy(network_size, vec=vec)
		self.enemy.assign_sim_info(play_area=38, stage_rad=30, bomb_area=40) # assign the info of the game (stage size, playable area...)
		self.danuri_enemy.FindComponentByType("TransformGroup").SetPosition(self._init_pos)


	def move(self, player_pos):
		bomb_list = self.bomb_con_actor.danuri_bomb_list # The list of the bomb exist on the game
		self.enemy.move(bomb_list, player_pos)

		# move danuri enemy
		self._pos.x = self.enemy.pos[0]
		self._pos.z = self.enemy.pos[1]
		self.danuri_enemy.FindComponentByType("TransformGroup").SetPosition(self._pos)


	def change_show(self, value):
		self.danuri_enemy.PropInstance.SetShow(value)