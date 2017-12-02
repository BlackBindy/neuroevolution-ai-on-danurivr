from .player import Player
from .simulation import Simulation

class Simulator:
	def __init__(self, total_frames, player_pos, sim_list, fps=60, play_area=38, stage_rad=30, bomb_area=40):
		self.sim_list = sim_list
		self.sim_num = len(sim_list)

		self.total_frames = total_frames
		self.fps = fps
		self.play_area = play_area
		self.stage_rad = stage_rad
		self.bomb_area = bomb_area

		# Private
		self.__cur_frame = 0
		self.__rank = []

	def run(self):		
		dead_enemies = 0
		while (self.__cur_frame < self.total_frames and dead_enemies < self.sim_num):
			for i in range(self.sim_num):
				# Append log list if there is no log for the enemy yet

				# Fetch current enemy, player, and simulation
				sim = self.sim_list[i]
				player = sim.player
				enemy = sim.enemy

				# If cur enemy is already dead, no simulation is proceeded
				if enemy.is_dead:
					continue


				# Move the player, it will shoot a bomb randomly
				player.move(enemy.pos)

				# Move the bombs and remove the ones whose position is too far
				'''
				removed_bombs = []
				for bomb in sim.get_bomb_list():
					bomb.move()

					# Destroy a bomb if it is out of the bomb area
					if (bomb.pos[0]**2 + bomb.pos[1]**2) > self.bomb_area**2:
						removed_bombs.append(bomb)

					# If a bomb hits the enemy, enemy dies
					dist_x = bomb.pos[0] - enemy.pos[0]
					dist_y = bomb.pos[1] - enemy.pos[1]
					dist = (dist_x**2 + dist_y**2)
					if dist < (bomb.rad+enemy.rad)**2:
						enemy.is_dead = True
						self.__rank.append(i)
						dead_enemies += 1

				sim.remove_bombs(removed_bombs)
				'''

				# Move the enemies and kill the ones who is hit by a bomb
				enemy.move(sim.get_bomb_list(), player.pos)

				# Increase the current frame count of the simulation by one
				sim.inc_frame_count()

			# Increase the frame of the simulator	
			self.__cur_frame += 1

		# All the survivors are added into the rank list
		for sim in self.sim_list:
			if sim.enemy.is_dead == False:
				self.__rank.append(sim.id)

		# Reverse the rank list (descending order on survival time)
		self.__rank.reverse()		

		# Print the final log
		for i in range(self.sim_num):
			if self.print_rank == -1 or self.print_rank > i:
				print(self.__log_list[self.__rank[i]])
			else:
				break

		# Print the final results
		print("Final Results: ")
		sum_frame_count = 0
		for i in self.__rank:
			frame_count = self.sim_list[i].get_frame_count()
			survival_time = frame_count/self.fps
			sum_frame_count += frame_count
			bomb_count = self.sim_list[i].player.bomb_count
			print("%3d has survived %6.2fseconds | Bomb count: %3d"%(i, survival_time, bomb_count))
		print()
		return sum_frame_count

	def fetch_top_enemies(self, num):
		if len(self.__rank) == 0:
			raise IndexError("Enemies are not ranked yet")
		return [self.sim_list[i].enemy for i in self.__rank[:num]]