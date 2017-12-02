import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from simulator.simulator import Simulator

class DanuriSimulator(Actor.Actor):
	def __init__(self):
		self.sim = Container(0)
		self.total_frames = 600

	def OnCreate(self, uid):
		self.sim_script = self.sim.FindComponentByType("ScriptComponent")
		self.sim_actor = self.sim_script.GetActor()

		self.sim_list = [self.sim_actor]
		self.simulator = Simulator(self.total_frames, (0, -38), [self.sim_list])