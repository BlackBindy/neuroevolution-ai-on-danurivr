import math
import Math3d
import sys

class ControllPlayer(Actor.Actor):
	def __init__(self):
		self.cam = Container(0)
		self.enemy = Container(0)
		self.bomb_con = Container(0)

		self._pos = Math3d.Vector3(0)
		self._targetDir = Math3d.Vector3(0)
		self._radius = 38
		self._angle = 0
		self._look = 0
		self._targetDir = (0,0,0)
		self._bombCount = 0
		self._enemyR = 2.0
		self._ballR = 0.5
		self._distance = self._enemyR + self._ballR

	def OnCreate(self, uid):
		self._radius = 38
		self._angle = 0
		self._pos.y = self.cam.FindComponentByType("TransformGroup").GetPosition().y
		self._Up = self.cam.FindComponentByType("TransformGroup").GetUp()
		self._look = 0
		self._targetDir = (0,0,0)
		self._bombCount = 0

		self._enemyR = 2.0
		self._ballR = 0.5
		self._distance = self._enemyR + self._ballR
		self.bomb_con.AddNewComponent("TransformGroup")
		self.bomb_con_script = self.bomb_con.FindComponentByType("ScriptComponent")
		self.bomb_con_actor = self.bomb_con_script.GetActor()
		return 0

	def Update(self):
		#move Camera
		self._pos.x = self._radius * math.cos(math.radians(self._angle))
		self._pos.z = self._radius * math.sin(math.radians(self._angle))
		
		self.cam.FindComponentByType("TransformGroup").SetPosition(self._pos)
		#Camera look at
		self._targetDir = self.GetLocalDir(self._pos)
		self.cam.FindComponentByType("TransformGroup").LookAtLocalDirection(self._targetDir)
		
		return 0

	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		if (msg == "KeyDown") :
			if (number == 37): #left arrow
				self._angle -= 1
			elif (number == 39) : #right arrow
				self._angle += 1
			elif (number == 38): #up arrow
				self._look += 0.5
			elif (number == 40): #down arrow
				self._look -= 0.5
			elif (number == 32):	#space
				self.Shoot(self._targetDir, self._pos)

		self._pos.x = self._radius * math.cos(math.radians(self._angle))
		self._pos.z = self._radius * math.sin(math.radians(self._angle))
		return 0


	def GetLocalDir(self, v1):
		temp = Math3d.Vector3(0)
		v = Math3d.Vector3(0)

		#Get local direction of (0,0,0)
		temp.x = -v1.x
		temp.y = 0
		temp.z = -v1.z

		#Calculate rotation
		v.y = temp.y
		v.x = temp.x * math.cos(math.radians(self._look)) - temp.z * math.sin(math.radians(self._look))
		v.z = temp.x * math.sin(math.radians(self._look)) + temp.z * math.cos(math.radians(self._look))
		return v

	def Shoot(self, direction, pos):
		direction.Normalize()
		self.bomb_con_actor.AddDanuriBomb(pos, direction)

def Getdistance(v1, v2):
	distance = float(0)
	distance = math.sqrt(math.pow(v1.x-v2.x, 2) + math.pow(v1.y-v2.y, 2) + math.pow(v1.z-v2.z, 2))
	return distance