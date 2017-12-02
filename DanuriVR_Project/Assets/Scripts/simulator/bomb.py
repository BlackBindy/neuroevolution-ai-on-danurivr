class Bomb:
	def __init__(self, position, direction, radius=0.5, speed=1):
		self.pos = position
		self.dir = direction # direction should be normalized
		self.rad = radius
		self.speed = speed

	def move(self):
		self.pos = (self.pos[0] + (self.dir[0] * self.speed), self.pos[1] + (self.dir[1] * self.speed))