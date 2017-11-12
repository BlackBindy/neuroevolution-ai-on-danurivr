from .simulation import Simulation
from .player import Player

class Simulator:
	def __init__(self, total_frames, player_pos):
		self.sim = Simulation(total_frames)
		self.player = Player(self.sim, player_pos)

	def run(self):
		while (self.sim.get_frame_count() <= self.sim.total_frames):
			self.player.move()
			self.sim.inc_frame_count()
			# print(self.player.position)
			for bomb in self.sim.get_bomb_list():
				bomb.move()
