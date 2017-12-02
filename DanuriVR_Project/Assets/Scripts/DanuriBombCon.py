import math
import Math3d

class DanuriBombCon(Actor.Actor):
	def __init__(self):
		self.enemy = Container(0)
		self.danuri_bomb_con = Container(0)
		self.danuri_bomb_list = []
		return

	def OnCreate(self, uid):
		self.enemy_script = self.enemy.FindComponentByType("ScriptComponent")
		self.enemy_actor = self.enemy_script.GetActor()

		self._enemyR = 2.0;
		self._ballR = 0.5;
		self._distance = self._enemyR + self._ballR
		self._bomb_area = 40
		#print(uid)
        #self.UID = uid
		#print(self.container)
		return 0

	def Update(self):
		if self.enemy_actor.enemy.is_dead == True:
			return 0

		next_bomb_list = []

		for bomb in self.danuri_bomb_list:
			obj = bomb[0]
			direction = bomb[1]

			pos = obj.FindComponentByType("TransformGroup").GetPosition()
			obj.FindComponentByType("TransformGroup").SetPosition(pos + direction)

			#check collision
			new_pos = obj.FindComponentByType("TransformGroup").GetPosition()
			if Getdistance(new_pos, self.enemy.FindComponentByType("TransformGroup").GetPosition()) < self._distance:
				self.enemy_actor.enemy.is_dead = True
				self.danuri_bomb_con.DeleteChild(self.danuri_bomb_con.GetChildIndex(obj))
				print("Collision!")
			elif Getdistance(new_pos, Math3d.Vector4(0,new_pos.y,0)) > self._bomb_area:
				self.danuri_bomb_con.DeleteChild(self.danuri_bomb_con.GetChildIndex(obj))
				print("Out of stage!")
			else:
				next_bomb_list.append(bomb)

		self.danuri_bomb_list = next_bomb_list

	def AddDanuriBomb(self, pos, direction):
		if self.enemy_actor.enemy.is_dead == True:
			return 0

		new_bomb = self.danuri_bomb_con.LoadPrefab("$project/Assets/Bomb.prefab")
		new_bomb.PropInstance.SetShow(True)
		new_bomb.FindComponentByType("TransformGroup").SetPosition(pos + 0.5 * direction)
		self.danuri_bomb_list.append((new_bomb, direction))

def Getdistance(v1, v2):
	distance = float(0)
	distance = math.sqrt(math.pow(v1.x-v2.x, 2) + math.pow(v1.y-v2.y, 2) + math.pow(v1.z-v2.z, 2))
	return distance