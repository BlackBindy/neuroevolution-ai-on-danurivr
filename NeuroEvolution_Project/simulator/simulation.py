class Simulation:
	def __init__(self, id):
		self.id = id
		self.player = None
		self.enemy = None

		# private
		self.__bomb_list = []
		self.__frame_count = 0

	def assign_player(self, player):
		self.player = player

	def assign_enemy(self, enemy):
		self.enemy = enemy

	def get_bomb_list(self):
		return self.__bomb_list

	def add_bomb(self, bomb):
		self.__bomb_list.append(bomb)

	def remove_bombs(self, bombs):
		if (len(bombs) > 0):
			for bomb in bombs:
				self.__bomb_list.remove(bomb)

	def get_frame_count(self):
		return self.__frame_count

	def inc_frame_count(self):
		self.__frame_count += 1