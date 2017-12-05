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
		self.sim6 = Container(0)
		self.sim7 = Container(0)
		self.sim8 = Container(0)
		self.sim9 = Container(0)
		self.sim10 = Container(0)
		self.total_frames = 1800
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
		self.population = 10
		self.crossover_prob = 0.4
		self._crossover_num = int(self.population * self.crossover_prob)
		self.mutation_prob = 0.001
		self.g = 0

		#GUI
		self.generation_label = Container(0)

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
		self.sim6_script = self.sim6.FindComponentByType("ScriptComponent")
		self.sim6_actor = self.sim6_script.GetActor()
		self.sim7_script = self.sim7.FindComponentByType("ScriptComponent")
		self.sim7_actor = self.sim7_script.GetActor()
		self.sim8_script = self.sim8.FindComponentByType("ScriptComponent")
		self.sim8_actor = self.sim8_script.GetActor()
		self.sim9_script = self.sim9.FindComponentByType("ScriptComponent")
		self.sim9_actor = self.sim9_script.GetActor()
		self.sim10_script = self.sim10.FindComponentByType("ScriptComponent")
		self.sim10_actor = self.sim10_script.GetActor()

		self.sim_list = [self.sim1_actor, self.sim2_actor, self.sim3_actor, self.sim4_actor, self.sim5_actor, self.sim6_actor, self.sim7_actor, self.sim8_actor, self.sim9_actor, self.sim10_actor]
		self.sim_num = len(self.sim_list)
		self.is_all_created = False

		self.generation_label.FindComponentByType("EGuiLabel").PropertyEGuiLabel.SetText("Generation : " + str(self.g))

	def Update(self):
		if self.is_all_created == False:
			self.is_all_created = True
			for sim in self.sim_list:
				self.is_all_created = self.is_all_created and self.is_on_create_done(sim)
		elif self.g >= self.generation:
			return 0
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
					frame_vec = []
					for sim in self.__rank:
						sum_frame_count += sim.get_frame()
						frame_vec.append(sim.get_frame())
					enemy_list = self.get_next_generation(self.g, sum_frame_count)

					result_str = ""
					for frame in frame_vec:
						result_str += "[%4.2fsec] "%(frame/60)
					print("Result: " + result_str)

					# Start next generation
					self.g += 1
					self.generation_label.FindComponentByType("EGuiLabel").PropertyEGuiLabel.SetText("Generation : " + str(self.g))
					for i in range(len(self.sim_list)):
						sim = self.sim_list[i]
						sim.enemy_actor.assign_enemy(enemy=enemy_list[i])
						sim.enemy_actor.reset_state()
						sim.player_actor.reset_state()
						sim.bomb_con_actor.reset_bomb_list()
						sim.reset_frame()
						self.__rank = []

					self.__cur_frame = 0
					self.__dead_enemies = 0
					self.__is_done = False


	# --------------------------------------------- #
	# Simulator                                     #
	# --------------------------------------------- #

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
			result = sim.player_actor.is_created & sim.enemy_actor.is_created
		return result


	# --------------------------------------------- #
	# Genetic Algorithm                             #
	# --------------------------------------------- #

	def get_next_generation(self, g, sum_frame_count):		
		next_gen = []

		# Create offsprings
		for c in range(self._crossover_num):
			# Selection
			parent1 = self.selection(sum_frame_count)
			parent2 = self.selection(sum_frame_count)

			# Crossover
			offspring = self.crossover(parent1, parent2)

			# Mutation
			self.mutation(offspring)
			next_gen.append(offspring)

		# Fill the rest of next gen list with the old parents
		survivor_num = self.population-self._crossover_num
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
