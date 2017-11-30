from simulator.simulator import Simulator
from simulator.enemy import Enemy
from network import numeric_components as num
import random as rd

class GeneticAlgorithm:
	def __init__(self, population=10, crossover_prob=0.4, generation=10, mutation_prob=0.001, network_size=[6, 8, 8, 2], total_frames=600, player_start_pos=(0, -38)):
		self.population = population
		if crossover_prob > 1:
			raise IndexError("Crossover probability can not exceed 1.0")
		elif crossover_prob < 0:
			raise IndexError("Crossover probability should be larger than or equals to 0.0")
		self.crossover_num = int(population * crossover_prob)
		self.generation = generation
		self.mutation_prob = mutation_prob
		self.network_size = network_size
		self.total_frames = total_frames
		self.player_start_pos = player_start_pos

	def run(self):
		best_enemies = []

		# Initialization
		enemy_list = []
		for p in range(self.population):
			enemy_list.append(Enemy(self.network_size))

		# Loop over generation
		for g in range(self.generation):
			print("[Generation #%d]"%(g))
			simulator, sum_frame_count = self.evaluation(enemy_list)
			best_enemies.append(simulator.fetch_top_enemies(1)[0])
			next_gen = []

			# Create offsprings
			for c in range(self.crossover_num):
				# Selection
				parent1 = self.selection(simulator, sum_frame_count)
				parent2 = self.selection(simulator, sum_frame_count)

				# Crossover
				offspring = self.crossover(parent1, parent2)

				# Mutation
				self.mutation(offspring)
				next_gen.append(offspring)

			# Fill the rest of next gen list with the old parents
			survivor_num = self.population-self.crossover_num
			for enemy in simulator.fetch_top_enemies(survivor_num):
				next_gen.append(enemy.nn.vectorize())

			# Set the new generation as the next enemy list
			if g < self.generation - 1:
				enemy_list = []
				for n in range(self.population):
					enemy_list.append(Enemy(self.network_size, vec=next_gen[n]))

		return best_enemies


	def evaluation(self, enemy_list):
		simulator = Simulator(self.total_frames, self.player_start_pos, enemy_list, print_rank=0)
		sum_frame_count = simulator.run()
		return simulator, sum_frame_count

	# Roulette Wheel Selection
	def selection(self, simulator, sum_frame_count):
		sel_point = rd.randrange(sum_frame_count)
		accum = 0
		for sim in simulator.sim_list:
			frame_count = sim.get_frame_count()
			if(accum <= sel_point and accum + frame_count > sel_point):
				return sim.enemy.nn.vectorize()
			accum += frame_count

		return sim.enemy.nn.vectorize()

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