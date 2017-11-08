from simulator.player import Player
import math

a = Player((0, -38))

'''
# Firing test
for i in range(500):
	a.move()
'''

# Moving & firing test
print(a.get_cur_velocity())
print(a.position)
for i in range(100):
	a.move()
	print(a.position)
	#print(math.sqrt(a.position[0]**2 + a.position[1]**2))