class Enemy:
	def __init__(self, neural_net, position=(0, 0), velocity=(0, 0), radius=2):
		self.neural_net = neural_net
		self.position = position
		self.velocity = velocity
		self.radius = radius