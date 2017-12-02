import random as rd
import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from simulator.simulator import Simulator
from simulator.enemy import Enemy
import network.numeric_components as num

class DanuriSimulator(Actor.Actor):
	def __init__(self):
		self.sim1 = Container(0)
		self.sim2 = Container(0)
		self.sim3 = Container(0)
		self.sim4 = Container(0)
		self.sim5 = Container(0)
		self.total_frames = 600
		self.fps = 60
		self.play_area = 38
		self.stage_rad = 30
		self.bomb_area = 40

		# Private
		self.__cur_frame = 0
		self.__rank = []
		self.__dead_enemies = 0
		self.__is_done = False

		# Genetic algorithm
		self.network_size = [8, 8, 6, 6]
		self.generation = 10
		self.population = 5
		self.crossover_num = 2
		self.mutation_prob = 0.001
		self.g = 0


	def OnCreate(self, uid):
		self.sim1_script = self.sim1.FindComponentByType("ScriptComponent")
		self.sim1_actor = self.sim1_script.GetActor()
		self.sim2_script = self.sim2.FindComponentByType("ScriptComponent")
		self.sim2_actor = self.sim2_script.GetActor()
		self.sim3_script = self.sim3.FindComponentByType("ScriptComponent")
		self.sim3_actor = self.sim3_script.GetActor()
		self.sim4_script = self.sim4.FindComponentByType("ScriptComponent")
		self.sim4_actor = self.sim4_script.GetActor()
		self.sim5_script = self.sim5.FindComponentByType("ScriptComponent")
		self.sim5_actor = self.sim5_script.GetActor()

		self.sim_list = [self.sim1_actor, self.sim2_actor, self.sim3_actor, self.sim4_actor, self.sim5_actor]
		self.sim_num = len(self.sim_list)
		self.is_all_created = False


	def Update(self):
		if self.is_all_created == False:
			self.is_all_created = True
			for sim in self.sim_list:
				self.is_all_created = self.is_all_created and self.is_on_create_done(sim)
		else:
			if self.__is_done == False and self.__cur_frame < self.total_frames and self.__dead_enemies < self.sim_num:
				self.__dead_enemies = self.run()
				self.__cur_frame += 1
			else:
				if self.__is_done == False:
					self.__is_done = True

					# Add survivors into the rank
					for sim in self.sim_list:
						if sim.enemy_actor.is_dead == False:
							self.__rank.append(sim)

					# Reverse the rank
					self.__rank.reverse()

					# Genetic algorithm
					sum_frame_count = 0
					for sim in self.__rank:
						sum_frame_count += sim.get_frame()
					enemy_list = self.get_next_generation(self.g, sum_frame_count)
					print(len(enemy_list))

					self.g += 1




	def get_next_generation(self, g, sum_frame_count):		
		next_gen = []

		# Create offsprings
		for c in range(self.crossover_num):
			# Selection
			parent1 = self.selection(sum_frame_count)
			parent2 = self.selection(sum_frame_count)

			# Crossover
			offspring = self.crossover(parent1, parent2)

			# Mutation
			self.mutation(offspring)
			next_gen.append(offspring)

		# Fill the rest of next gen list with the old parents
		survivor_num = self.population-self.crossover_num
		for sim in self.__rank[:survivor_num]:
			next_gen.append(sim.enemy_actor.enemy.nn.vectorize())

		# Set the new generation as the next enemy list
		enemy_list = []
		if g < self.generation - 1:
			for n in range(self.population):
				enemy_list.append(Enemy(self.network_size, vec=next_gen[n]))
		return enemy_list

	# Roulette Wheel Selection
	def selection(self, sum_frame_count):
		sel_point = rd.randrange(sum_frame_count)
		accum = 0
		for sim in self.__rank:
			frame_count = sim.get_frame()
			if(accum <= sel_point and accum + frame_count > sel_point):
				return sim.enemy_actor.enemy.nn.vectorize()
			accum += frame_count

		return sim.enemy_actor.enemy.nn.vectorize()

	# Single-point Crossover
	def crossover(self, parent1, parent2):
		length = len(parent1)
		offspring = []
		crossover_point = rd.randrange(length-1) # [0, length-2]
		for i in range(length):
			if i <= crossover_point:
				offspring.append(parent1[i])
			else:
				offspring.append(parent2[i])

		return offspring


	def mutation(self, offspring):
		for i in range(len(offspring)):
			if rd.random() <= self.mutation_prob:
				offspring[i] = num.get_rand()



		'''
		def run_all(self):		
			self.on_simulation = True

			dead_enemies = 0
			while (self.__cur_frame < self.total_frames and dead_enemies < self.sim_num):
				dead_enemies = self.run()

			self.on_simulation = False
		'''
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
		dead_enemies = 0

		for i in range(self.sim_num):
			# Fetch current enemy, player, and simulation
			sim = self.sim_list[i]
			player = sim.player_actor
			enemy = sim.enemy_actor

			# If cur enemy is already dead, no simulation is proceeded
			if enemy.is_dead:
				dead_enemies += 1
				if not sim in self.__rank:
					self.__rank.append(sim)
				continue

			# Move the player, it will shoot a bomb randomly
			player.move(enemy.pos)
			sim.increase_frame()

		return dead_enemies

	def fetch_top_enemies(self, num):
		if len(self.__rank) == 0:
			raise IndexError("Enemies are not ranked yet")
		return [self.sim_list[i].enemy for i in self.__rank[:num]]

	def is_on_create_done(self, sim):
		result = False
		if sim.is_created == True:
			print("player:",sim.player_actor.is_created)
			print("enemy:",sim.enemy_actor.is_created)
			result = sim.player_actor.is_created & sim.enemy_actor.is_created
			#print("result:", result)
		return result