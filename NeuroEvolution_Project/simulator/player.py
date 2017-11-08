import random as rd
import math

class Player:
	fps = 60

	def __init__(self, position, velocity=1, move_cycle=30, fire_rate=1, fire_cycle=3, play_area=38):
		self.position = position
		self.velocity = velocity # velocity in degree
		self.move_cycle = move_cycle # least number of frames that player should maintain the velocity
		self.fire_rate = fire_rate * self.fps # minimum number of frames until the next fire
		self.fire_cycle = fire_cycle * self.fps # maximum number of frames until the next fire
		self.play_area = play_area

		# private
		self.__frame_count = 1
		self.assign_velocity()
		self.assign_next_fire()

	def move(self):
		# Shoot a bomb (decrease next_fire by 1, when it reaches 0 then fire)
		if(self.__next_fire > 0):
			self.__next_fire -= 1
		else:
			self.fire()
			self.assign_next_fire()

		# Change the velocity every n frames (n: move_cycle)
		if(self.__frame_count % self.move_cycle == 0):
			self.assign_velocity()

		# Calculate the new position
		cos_v = math.cos(self.__cur_velocity)
		sin_v = math.sin(self.__cur_velocity)
		new_x = (cos_v * self.position[0]) - (sin_v * self.position[1])
		new_y = (sin_v * self.position[0]) + (cos_v * self.position[1])
		self.position = (new_x, new_y)

		# Increase frame_count by 1
		self.__frame_count += 1

	# Assign a new velocity in RADIAN (not in degree)
	def assign_velocity(self):
		self.__cur_velocity = math.radians(rd.randint(-self.velocity, self.velocity))

	# Assign a new next_shoot (framewise countdown for the next fire)
	def assign_next_fire(self):
		self.__next_fire = rd.randint(self.fire_rate, self.fire_cycle)

	# Fire a bomb
	def fire(self):
		print('fire!!!')

	###### Test purpose (to be removed)
	def get_frame_count(self):
		return self.__frame_count

	def get_cur_velocity(self):
		return self.__cur_velocity

	def get_next_fire(self):
		return self.__next_fire