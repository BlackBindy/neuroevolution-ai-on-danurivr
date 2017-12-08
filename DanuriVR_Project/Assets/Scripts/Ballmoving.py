import math
import Math3d

class Ballmoving(Actor.Actor):
	def __init__(self):
		self.ball = Container(0)
		self._rot = Math3d.Vector3(0)
		return

	def OnCreate(self, uid):
		self._time = 0
		self._rot.x = 0
		self._rot.y = 0
		return 0

	def Update(self):
		self._time += 1

		if(self._time % 4 == 0) :
			self._rot.z = 10
		else (self._time % 3 == 2):
			self._rot.z = -10
		else : 
			self._rot.z = 0

		self.ball.FindComponentByType("TransformGroup").SetRotation(self._rot)
		return 0