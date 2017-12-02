import math
import Math3d
import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from simulator.player import Player

class DanuriLearningPlayer(Actor.Actor):
	def __init__(self):
		self.con = Container(0)
		self.bomb_con = Container(0)
		self.is_created = False

	def OnCreate(self, uid):
		self.bomb_con_script = self.bomb_con.FindComponentByType("ScriptComponent")
		self.bomb_con_actor = self.bomb_con_script.GetActor()

		self.transform_group = self.con.FindComponentByType("TransformGroup")
		self.pos = self.transform_group.GetPosition()
		self.init_pos = self.pos
		self.player = Player(self.bomb_con_actor, (self.pos.x, self.pos.z), self.pos.y, 60, 38)
		self.is_created = True

	def move(self, enemy_pos):
		enemy_pos = (enemy_pos.x, enemy_pos.z)
		self.player.move(enemy_pos)
		self.pos.x = self.player.pos[0]
		self.pos.z = self.player.pos[1]
		self.transform_group.SetPosition(self.pos)

	def reset_state(self):
		self.player.reset_state()
		self.pos = self.init_pos
		self.transform_group.SetPosition(self.pos)