from .simulation import Simulation
from .player import Player
from .enemy import Enemy

class Simulator:
	def __init__(self, total_frames, player_pos, enemy_num, network_size):
		self.sim = Simulation(total_frames)
		self.player = Player(self.sim, player_pos)
		self.enemy_list = [Enemy(network_size, self.sim.stage_rad) for i in range(enemy_num)]

	def run(self):
		while (self.sim.get_frame_count() <= self.sim.total_frames):
			# Move the player
			self.player.move()
			# print(self.player.pos)

			# Move the bombs and remove the ones whose position is too far
			# print (len(self.sim.get_bomb_list())) ###########
			removed_bombs = []
			for bomb in self.sim.get_bomb_list():
				bomb.move()
				# print(str(bomb.pos) + " / " + str((bomb.pos[0]**2 + bomb.pos[1]**2)))
				if ((bomb.pos[0]**2 + bomb.pos[1]**2) > self.sim.bomb_area**2): # bomb position > accepted area
					removed_bombs.append(bomb)
			self.sim.remove_bombs(removed_bombs)

			# Move the enemies and kill the ones who is hit by a bomb
			for enemy in self.enemy_list:
				enemy.move(self.sim.get_bomb_list(), self.player.pos)
				#print("Enemy Position: %.4f, %.4f"%(enemy.pos[0], enemy.pos[1]))

			# Increase the frame count by one
			self.sim.inc_frame_count()
