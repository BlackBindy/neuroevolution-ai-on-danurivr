from simulator.simulator import Simulator
from simulator.enemy import Enemy

class GeneticAlgorithm:
	def __init__(self, population=10, gen=10, network_size=[6, 8, 8, 2], total_frames=600, player_start_pos=(0, -38)):
		self.population = population
		self.gen = gen
		self.network_size = network_size
		self.total_frames = total_frames
		self.player_start_pos = player_start_pos

	def run(self):
		# Initialization
		enemy_list = []
		for i in range(self.population):
			enemy_list.append(Enemy(self.network_size))

		# Loop
		simulator = self.evaluation(enemy_list)
		top_enemies = self.selection(simulator)

	def evaluation(self, enemy_list):
		simulator = Simulator(self.total_frames, self.player_start_pos, enemy_list, print_rank=1)
		simulator.run()
		return simulator

	def selection(self, simulator):
		return simulator.fetch_top_enemies(4)

	def crossover(self, enemy_list):
		pass

	def mutation(self, enemy_list):
		pass