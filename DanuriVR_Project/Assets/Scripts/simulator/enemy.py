from network.neural_network import NeuralNetwork
import math

class Enemy:
	def __init__(self, network_size, vec=None, activation='tanh', position=(0, 0), radius=2, max_speed=2, max_bomb_dist=100, use_velocity=True):
		self.nn = NeuralNetwork(network_size, activation=activation, vec=vec)
		self.play_area = None
		self.stage_rad = None
		self.bomb_area = None
		self.pos = position
		self.rad = radius
		self.amplifier = max_speed / math.sqrt(2) # to amplify the speed from [-1, 1] to [-max_speed, max_speed]
		self.max_bomb_dist = max_bomb_dist
		self.use_velocity = use_velocity # True: NN result represents velocity, False: NN result represents acceleration
		self.is_dead = False

		# private		
		self._vel = (0, 0) # velocity

	def assign_sim_info(self, play_area, stage_rad, bomb_area):
		self.play_area = play_area
		self.stage_rad = stage_rad
		self.bomb_area = bomb_area

	def move(self, bomb_list, player_pos):
		# Distance of the enemy from the origin
		e_x = self.pos[0]
		e_y = self.pos[1]
		e_d = math.sqrt(e_x**2 + e_y**2)
		e_x_normal = e_x / self.stage_rad # Further the enemy position, larger the value
		e_y_normal = e_y / self.stage_rad

		# Distance from the wall (not used?)
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
		p_max_dist = self.play_area + self.stage_rad
		p_x_normal = p_x / p_max_dist # Closer the distance to the player, larger the value
		p_y_normal = p_y / p_max_dist

		# Distance from the bombs & Run the network
		v_x = 0
		v_y = 0
		b_max_dist = self.play_area + self.bomb_area
		bomb_num = len(bomb_list)
		if (bomb_num > 0): # Run the network for each bomb and take an average velocity of the results
			for bomb in bomb_list:
				obj = bomb[0]
				pos = obj.FindComponentByType("TransformGroup").GetPosition()
				btoe_x = pos.x - e_x
				btoe_y = pos.z - e_y
				btoe_d = math.sqrt(btoe_x**2 + btoe_y**2)
				b_d = btoe_d - self.rad - 0.5
				if (btoe_d > 0.001):
					b_x = b_d * (btoe_x/btoe_d) # d * cos(theta)
					b_y = b_d * (btoe_y/btoe_d) # d * sin(theta)
				else: # to prevent division by zero (but this case will not happen)
					b_x = b_d
					b_y = b_d
				b_x_normal = b_x / b_max_dist
				b_y_normal = b_y / b_max_dist
				v = self.nn.run([e_x_normal, e_y_normal, p_x_normal, p_y_normal, b_x_normal, b_y_normal])
				v_x += v[0]
				v_y += v[1]
				#print("-------------------------------%.4f, %.4f"%(v[0], v[1]))
			# Take the average velocity
			if self.use_velocity:
				self._vel = (v_x/bomb_num, v_y/bomb_num)
			else:
				vel0 = max(min(1.0, self._vel[0] + v_x/bomb_num), -1.0)
				vel1 = max(min(1.0, self._vel[1] + v_y/bomb_num), -1.0)
				self._vel = (vel0, vel1)
		else: # If there is no bomb, set the distance as the distance to the player
			b_x = p_x
			b_y = p_y
			b_x_normal = b_x / b_max_dist
			b_y_normal = b_y / b_max_dist
			# b_x = self.max_bomb_dist
			# b_y = self.max_bomb_dist
			v = self.nn.run([e_x_normal, e_y_normal, p_x_normal, p_y_normal, b_x_normal, b_y_normal]) # using from origin
			# v = self.nn.run([w_x, w_y, p_x, p_y, b_x, b_y]) # using to wall
			if self.use_velocity:
				self._vel = (v[0], v[1])
			else:
				vel0 = max(min(1.0, self._vel[0] + v[0]), -1.0)
				vel1 = max(min(1.0, self._vel[0] + v[1]), -1.0)
				self._vel = (vel0, vel1)

		# Move
		log = "Network Inputs: O (%.3f, %.3f), P (%.3f, %.3f), B (%.3f, %.3f)"%(e_x_normal, e_y_normal, p_x_normal, p_y_normal, b_x_normal, b_y_normal)
		#print ("%.4f, %.4f, %.4f, %.4f, %.4f, %.4f"%(e_x, e_y, p_x, p_y, b_x, b_y))
		# print ("%.4f, %.4f, %.4f, %.4f, %.4f, %.4f"%(w_x, w_y, p_x, p_y, b_x, b_y))
		# print("original vel: " + str(self._vel))
		self._vel = (self._vel[0]*self.amplifier, self._vel[1]*self.amplifier) # [-1, 1] -> [-max_speed, max_speed]
		# print("to origin: %.3f, to wall: %.3f, to player: %.3f"%(e_d, w_d, p_d))
		log += "\nNetwork Result: (%.3f, %.3f), Velocity: (%.3f, %.3f)"%(v[0], v[1], self._vel[0], self._vel[1])
		#print("Final Velocity: %.4f, %.4f"%(self._vel[0], self._vel[1]))
		pos = (e_x + self._vel[0], e_y + self._vel[1])
		#print("Final Position: %.4f, %.4f"%(pos[0], pos[1]))

		# If the new position is outside of the stage, there is no change on position
		if ((math.sqrt(pos[0]**2 + pos[1]**2) + self.rad) < self.stage_rad):
			self.pos = pos
			log += "\n----- Enemy Move -----"

		# Print the log
		return log