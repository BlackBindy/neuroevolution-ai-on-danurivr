#import math
#import Math3d

class DanuriBomb(Actor.Actor):
	def __init__(self):
		#self._pos = Math3d.Vector3(0)
		print("test-init")
		return

	def OnCreate(self, uid):
		#self.bomb = None
		print("test-OnCreate")
		return 0

	def Update(self):
		return 0
		#if self.bomb != None:
			# move bomb
			#self.bomb.move()
			#print("123")

			# move danuri bomb
			#self._pos.x = self.bomb.pos[0]
			#self._pos.z = self.bomb.pos[1]
			#self.transform_group.SetPosition(self._pos)
		

	def init_bomb(self, obj, position, direction, radius=0.5, speed=1):
		#self.transform_group = obj.FindComponentByType("TransformGroup")
		#self._pos.y = self.transform_group.GetPosition().y
		#self.bomb = Bomb(position, direction, radius, speed)
		print("done!")
		return