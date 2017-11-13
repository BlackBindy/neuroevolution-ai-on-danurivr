from .bomb import Bomb
import random as rd
import math

class Player:
	def __init__(self, simulation, position, speed=1, move_cycle=30, fire_rate=1, fire_cycle=3, play_area=38):
		self.sim = simulation
		self.pos = position
		self.speed = speed # speed in degree
		self.move_cycle = move_cycle # least number of frames that player should maintain the speed
		self.fire_rate = fire_rate * self.sim.fps # minimum number of frames until the next fire
		self.fire_cycle = fire_cycle * self.sim.fps # maximum number of frames until the next fire
		self.play_area = play_area

		# private
		self.assign_speed()
		self.assign_next_fire()

	def move(self):
		# Shoot a bomb (decrease next_fire by 1, when it reaches 0 then fire)
		if(self.__next_fire > 0):
			self.__next_fire -= 1
		else:
			self.fire()
			self.assign_next_fire()

		# Change the speed every n frames (n: move_cycle)
		if(self.sim.get_frame_count() % self.move_cycle == 0):
			self.assign_speed()

		# Calculate the new position
		cos_v = math.cos(self.__cur_speed)
		sin_v = math.sin(self.__cur_speed)
		new_x = (cos_v * self.pos[0]) - (sin_v * self.pos[1])
		new_y = (sin_v * self.pos[0]) + (cos_v * self.pos[1])
		self.pos = (new_x, new_y)

	# Assign a new speed in RADIAN (not in degree)
	def assign_speed(self):
		self.__cur_speed = math.radians(rd.randint(-self.speed, self.speed))

	# Assign a new next_shoot (framewise countdown for the next fire)
	def assign_next_fire(self):
		self.__next_fire = rd.randint(self.fire_rate, self.fire_cycle)

	# Fire a bomb
	def fire(self):
		enemy_pos = (0, 0) # TEMP
		to_enemy = (enemy_pos[0]-self.pos[0], enemy_pos[1]-self.pos[1]) # TEMP
		sqrt = math.sqrt(to_enemy[0]**2 + to_enemy[1]**2)
		to_enemy = (to_enemy[0]/sqrt, to_enemy[1]/sqrt)
		bomb = Bomb(self.pos, to_enemy)
		self.sim.add_bomb(bomb)
		print ("Fire!")

	###### Test purpose (to be removed)
	def get_cur_speed(self):
		return self.__cur_speed

	def get_next_fire(self):
		return self.__next_fire