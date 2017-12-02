import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from simulator.simulation import Simulation

class DanuriSimulation(Actor.Actor):
	def __init__(self):
		self.enemy = Container(0)
		self.player = Container(0)
		self.bomb_con = Container(0)

		self.enemy_actor = None
		self.player_actor = None

		self._frame_count = 0
		self.is_created = False

	def OnCreate(self, uid):
		self.enemy_script = self.enemy.FindComponentByType("ScriptComponent")
		self.enemy_actor = self.enemy_script.GetActor()
		self.player_script = self.player.FindComponentByType("ScriptComponent")
		self.player_actor = self.player_script.GetActor()
		
		self.bomb_con_script = self.bomb_con.FindComponentByType("ScriptComponent")
		self.bomb_con_actor = self.bomb_con_script.GetActor()
		self.is_created = True

	def increase_frame(self):
		self._frame_count += 1

	def get_frame(self):
		return self._frame_count