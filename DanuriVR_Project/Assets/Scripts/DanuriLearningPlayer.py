import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from simulator.player import Player

class DanuriLearningPlayer(Actor.Actor):
	def __init__(self):
		self.sim = Container(0)
		self.player = None

	def OnCreate(self, uid):
		self.sim_script = self.sim.FindComponentByType("ScriptComponent")
		self.sim_actor = self.sim_script.GetActor()

		self.player = Player(self.sim_actor.sim, (0, -38), 60, 38)