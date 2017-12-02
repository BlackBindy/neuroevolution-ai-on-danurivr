import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from simulator.simulator import Simulator
from simulator.enemy import Enemy

class DanuriSimulator(Actor.Actor):
	def __init__(self):
		self.sim = Container(0)
		self.total_frames = 600
		self.fps = 60
		self.play_area = 38
		self.stage_rad = 30
		self.bomb_area = 40

		# Private
		self.__cur_frame = 0
		self.__rank = []


	def OnCreate(self, uid):
		self.sim_script = self.sim.FindComponentByType("ScriptComponent")
		self.sim_actor = self.sim_script.GetActor()

		self.sim_list = [self.sim_actor]
		self.sim_num = len(self.sim_list)
		self.is_all_created = False


	def Update(self):
		if self.is_all_created == False:
			for sim in self.sim_list:
				self.is_all_created = self.is_on_create_done(sim)
		else:
			self.run()


	def run_all(self):		
		dead_enemies = 0
		while (self.__cur_frame < self.total_frames and dead_enemies < self.sim_num):
			self.run()

		# All the survivors are added into the rank list
		'''
		for sim in self.sim_list:
			if sim.enemy.is_dead == False:
				self.__rank.append(sim.id)
		'''

		# Reverse the rank list (descending order on survival time)
		'''
		self.__rank.reverse()		

		# Print the final log
		for i in range(self.sim_num):
			if self.print_rank == -1 or self.print_rank > i:
				print(self.__log_list[self.__rank[i]])
			else:
				break
		'''

		# Print the final results
		'''
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
		'''

	def run(self):
		for i in range(self.sim_num):
			# Append log list if there is no log for the enemy yet

			# Fetch current enemy, player, and simulation
			sim = self.sim_list[i]
			player = sim.player_actor
			enemy = sim.enemy_actor

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
			#enemy.move(sim.get_bomb_list(), player.pos)

			# Increase the current frame count of the simulation by one
			#sim.inc_frame_count()

		# Increase the frame of the simulator	
		self.__cur_frame += 1

	def fetch_top_enemies(self, num):
		if len(self.__rank) == 0:
			raise IndexError("Enemies are not ranked yet")
		return [self.sim_list[i].enemy for i in self.__rank[:num]]

	def is_on_create_done(self, sim):
		result = False
		if sim.is_created == True:
			#print("player:",sim.player_actor.is_created)
			#print("enemy:",sim.enemy_actor.is_created)
			result = sim.player_actor.is_created and sim.enemy_actor.is_created
			#print("result:", result)
		return result