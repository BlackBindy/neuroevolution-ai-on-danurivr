import math
import Math3d
import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from genetic.genetic import GeneticAlgorithm
from simulator.enemy import Enemy
from file_manager import *

class DanuriLearningEnemy(Actor.Actor):
	def __init__(self):
		self.danuri_enemy = Container(0)
		self.danuri_palyer = Container(0)
		self.bomb_con = Container(0)
		self.pos = Math3d.Vector3(0,0,0)
		self.enemy = None
		self.is_dead = False
		self.is_created = False


	def OnCreate(self, uid):
		self.bomb_con_script = self.bomb_con.FindComponentByType("ScriptComponent")
		self.bomb_con_actor = self.bomb_con_script.GetActor()

		self._init_pos = self.danuri_enemy.FindComponentByType("TransformGroup").GetPosition()
		self.pos.y = self.danuri_enemy.FindComponentByType("TransformGroup").GetPosition().y

		self.network_size = [8, 8, 6, 6]
		self.assign_enemy()
		self.is_created = True


	def Update(self):
		if self.enemy == None:
			return 0
		elif self.enemy.is_dead == True:
			self.is_dead = True	
			return 0
			
		danuri_palyer_pos = self.danuri_palyer.FindComponentByType("TransformGroup").GetPosition()
		danuri_palyer_pos = (danuri_palyer_pos.x, danuri_palyer_pos.z)
		#print(danuri_palyer_pos)
		self.move(danuri_palyer_pos)


	def move(self, player_pos):
		bomb_list = self.bomb_con_actor.danuri_bomb_list # The list of the bomb exist on the game
		self.enemy.move(bomb_list, player_pos)

		# move danuri enemy
		self.pos.x = self.enemy.pos[0]
		self.pos.z = self.enemy.pos[1]
		self.danuri_enemy.FindComponentByType("TransformGroup").SetPosition(self.pos)

	def change_show(self, value):
		self.danuri_enemy.PropInstance.SetShow(value)

	def assign_enemy(self, enemy=None):
		if enemy == None:
			self.enemy = Enemy(self.network_size)
		else:
			self.enemy = enemy
			print("yea")
		self.enemy.assign_sim_info(play_area=38, stage_rad=30, bomb_area=40) # assign the info of the game (stage size, playable area...)

	def reset_state(self):
		self.change_show(1)
		self.is_dead = False
		self.danuri_enemy.FindComponentByType("TransformGroup").SetPosition(self._init_pos)	