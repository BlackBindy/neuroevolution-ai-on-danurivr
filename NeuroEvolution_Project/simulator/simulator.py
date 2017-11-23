from .simulation import Simulation
from .player import Player
from .enemy import Enemy

class Simulator:
	def __init__(self, total_frames, player_pos, enemy_num, network_size, fps=60, play_area=38, stage_rad=30, bomb_area=40):
		self.sim_list = [Simulation(i) for i in range(enemy_num)]
		for sim in self.sim_list:
			sim.assign_player(Player(sim, player_pos, fps, play_area))
			sim.assign_enemy(Enemy(network_size, stage_rad, play_area, bomb_area))
		self.total_frames = total_frames
		self.enemy_num = enemy_num
		self.fps = fps
		self.play_area = play_area
		self.stage_rad = stage_rad
		self.bomb_area = bomb_area

		# Private
		self.__cur_frame = 0

	def run(self):		
		dead_enemies = 0
		while (self.__cur_frame < self.total_frames and dead_enemies < self.enemy_num):
			for i in range(self.enemy_num):
				# Fetch current enemy, player, and simulation
				sim = self.sim_list[i]
				player = sim.player
				enemy = sim.enemy

				# If cur enemy is already dead, no simulation is proceeded
				if enemy.is_dead:
					break

				# Test purpose
				print("[ ", i, " / ", sim.get_frame_count()," ]")
				
				# Move the player, it will shoot a bomb randomly
				player.move(enemy.pos)
				# print(self.player.pos)

				# Move the bombs and remove the ones whose position is too far
				# print (len(self.sim.get_bomb_list())) ###########
				removed_bombs = []
				for bomb in sim.get_bomb_list():
					bomb.move()
					# print(str(bomb.pos) + " / " + str((bomb.pos[0]**2 + bomb.pos[1]**2)))
					if ((bomb.pos[0]**2 + bomb.pos[1]**2) > self.bomb_area**2): # bomb position > accepted area
						removed_bombs.append(bomb)
				sim.remove_bombs(removed_bombs)

				# Move the enemies and kill the ones who is hit by a bomb
				enemy.move(sim.get_bomb_list(), player.pos)
				#print("Enemy Position: %.4f, %.4f"%(enemy.pos[0], enemy.pos[1]))

				# Increase the current frame count of the simulation by one
				sim.inc_frame_count()

				# Test purpose
				print ("Player: (%.3f, %.3f)"%(player.pos[0], player.pos[1]))
				print ("Enemy: (%.3f, %.3f)"%(enemy.pos[0], enemy.pos[1]))
				if len(sim.get_bomb_list()) > 0:
					print("")
					for bomb in sim.get_bomb_list():
						print ("Bomb: (%.3f, %.3f)"%(bomb.pos[0], bomb.pos[1]))
				print("====================================")

			# Increase the frame of the simulator	
			self.__cur_frame += 1
