import pickle

class DanuriEnemy:
	def __init__(self, network_size=[6, 6, 6, 2], vec=None, activation='tanh', position=(0, 0), radius=2, max_speed=2, max_bomb_dist=100, use_velocity=True):
		if vec != None:
			with open(vec, "rb") as fp:   # Unpickling
				vec = pickle.load(fp)
		self.enemy = Enemy(network_size, vec, activation, position, radius, max_speed, max_bomb_dist, use_velocity)

	def update(self):
		while self.enemy.is_dead != True:
			position = self.enemy.move(bomb_list, enemy_pos)
			# Do move
			# ex) game_object.position = position

	def move(self, bomb_list, enemy_pos):
		self.enemy.move(bomb_list, enemy_pos)
