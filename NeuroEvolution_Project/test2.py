from simulator.simulator import Simulator
from simulator.enemy import Enemy

enemy_num = 10
enemy_list = []
network_size = [6, 8, 8, 2]
for i in range(enemy_num):
	enemy_list.append(Enemy(network_size))

s = Simulator(600, (0, -38), enemy_list, print_rank=1)
s.run()

sub = s.fetch_top_enemies(4)