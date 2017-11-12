class Enemy:
	def __init__(self, neural_network, position=(0, 0), velocity=(0, 0), radius=2):
		self.nn = neural_network
		self.pos = position
		self.vel = velocity
		self.rad = radius