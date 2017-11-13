from network.neural_network import NeuralNetwork
import math

class Enemy:
	def __init__(self, network_size, stage_rad, activation='sigmoid', position=(0, 0), radius=2, max_speed=2 ,max_bomb_dist=100):
		self.nn = NeuralNetwork(network_size, activation=activation)
		self.stage_rad = stage_rad
		self.pos = position
		self.rad = radius
		self.amplifier = max_speed / math.sqrt(2) # to amplify the speed from [-1, 1] to [-max_speed, max_speed]
		self.max_bomb_dist = max_bomb_dist

		# private		
		self._vel = (0, 0) # velocity

	def move(self, bomb_list, player_pos):
		# Distance of the enemy from the origin
		e_x = self.pos[0]
		e_y = self.pos[1]
		e_d = math.sqrt(e_x**2 + e_y**2)

		# Distance from the wall
		w_d = self.stage_rad - e_d - self.rad
		if (e_d > 0.001):
			w_x = w_d * (e_x/e_d) # d * cos(theta)
			w_y = w_d * (e_y/e_d) # d * sin(theta)
		else: # to prevent division by zero
			w_x = w_d
			w_y = w_d

		# Distance from the player
		ptoe_x = player_pos[0] - e_x
		ptoe_y = player_pos[1] - e_y
		ptoe_d = math.sqrt(ptoe_x**2 + ptoe_y**2)
		p_d = ptoe_d - self.rad
		if (ptoe_d > 0.001):
			p_x = p_d * (ptoe_x/ptoe_d) # d * cos(theta)
			p_y = p_d * (ptoe_y/ptoe_d) # d * sin(theta)
		else: # to prevent division by zero (but this case will not happen)
			p_x = p_d
			p_y = p_d

		# Distance from the bombs & Run the network
		v_x = 0
		v_y = 0
		bomb_num = len(bomb_list)
		if (bomb_num > 0): # Run the network for each bomb and take an average velocity of the results
			for bomb in bomb_list:
				btoe_x = bomb.pos[0] - e_x
				btoe_y = bomb.pos[1] - e_y
				btoe_d = math.sqrt(btoe_x**2 + btoe_y**2)
				b_d = btoe_d - self.rad - bomb.rad
				if (btoe_d > 0.001):
					b_x = b_d * (btoe_x/btoe_d) # d * cos(theta)
					b_y = b_d * (btoe_y/btoe_d) # d * sin(theta)
				else: # to prevent division by zero (but this case will not happen)
					b_x = b_d
					b_y = b_d

				v = self.nn.run([w_x, w_y, p_x, p_y, b_x, b_y])
				v_x += v[0]
				v_y += v[1]
				#print("-------------------------------%.4f, %.4f"%(v[0], v[1]))
			self._vel = (v_x/bomb_num, v_y/bomb_num)
		else: # If there is no bomb, set the distance as max distance
			b_x = self.max_bomb_dist
			b_y = self.max_bomb_dist
			v = self.nn.run([w_x, w_y, p_x, p_y, b_x, b_y])
			self._vel = (v[0], v[1])

		# Move
		# print ("%.4f, %.4f, %.4f, %.4f, %.4f, %.4f"%(w_x, w_y, p_x, p_y, b_x, b_y))
		# print("original vel: " + str(self._vel))
		self._vel = (self._vel[0]*self.amplifier, self._vel[1]*self.amplifier) # [-1, 1] -> [-max_speed, max_speed]
		# print("Final Velocity: %.4f, %.4f"%(self._vel[0], self._vel[1]))
		pos = (e_x + self._vel[0], e_y + self._vel[1])
		if ((pos[0]**2 + pos[1]**2) < self.stage_rad):
			self.pos = pos
