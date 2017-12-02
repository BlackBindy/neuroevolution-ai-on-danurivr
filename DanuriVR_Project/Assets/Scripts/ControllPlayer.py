import math
import Math3d
import sys
sys.path.insert(0, EngineFileTool.GetProjectPath() + '/Assets/Scripts')
from simulator.bomb import Bomb

class ControllPlayer(Actor.Actor):
	def __init__(self):
		self.cam = Container(0)
		self.enemy = Container(0)
		self.bomb_con = Container(0)

		self._pos = Math3d.Vector3(0)
		self._targetDir = Math3d.Vector3(0)
		self._bombList = [];
		self._bomb_dirList = [];

	def OnCreate(self, uid):
		self._radius = 38
		self._angle = 0
		self._pos.y = self.cam.FindComponentByType("TransformGroup").GetPosition().y
		self._Up = self.cam.FindComponentByType("TransformGroup").GetUp()
		self._look = 0
		self._targetDir = (0,0,0)
		self._bombCount = 0;

		self._enemyR = 2.0;
		self._ballR = 0.5;
		self._distance = self._enemyR + self._ballR
		self.bomb_con.AddNewComponent("TransformGroup")
		return 0

	def Update(self):
		#move Camera
		self._pos.x = self._radius * math.cos(math.radians(self._angle))
		self._pos.z = self._radius * math.sin(math.radians(self._angle))
		
		self.cam.FindComponentByType("TransformGroup").SetPosition(self._pos)
		#Camera look at
		self._targetDir = self.GetLocalDir(self._pos)
		self.cam.FindComponentByType("TransformGroup").LookAtLocalDirection(self._targetDir)

		#check collision
		for i in range(len(self._bombList)):
			if(Getdistance(self._bombList[i].FindComponentByType("TransformGroup").GetPosition(), self.enemy.FindComponentByType("TransformGroup").GetPosition()) < self._distance):
				print("Collision!")


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
		#save target direction
		direction.Normalize()
		self._bomb_dirList.append(direction)

		#load prefab
		new_bomb = self.bomb_con.LoadPrefab("$project/Assets/Bomb.prefab")
		component = new_bomb.FindComponentByType("ScriptComponent")
		print(type(component.GetActor()))
		#actor = component.GetActor()
		#print(type(new_bomb))
		#print(type(actor))
		#create bomb
		#new_bomb.PropInstance.SetShow(True)
		#new_bomb.FindComponentByType("TransformGroup").SetPosition(pos + 0.5 * direction)
		#temp_pos = (pos.x, pos.z)
		#temp_dir = (direction.x, direction.z)
		#new_bomb.FindComponentByType("ScriptComponent").GetActor()#.init_bomb(new_bomb, temp_pos, temp_dir)
		self._bombList.append(new_bomb)

		self._bombCount += 1

def Getdistance(v1, v2):
	distance = float(0)
	distance = math.sqrt(math.pow(v1.x-v2.x, 2) + math.pow(v1.y-v2.y, 2) + math.pow(v1.z-v2.z, 2))
	return distance
'''
	def get_bomb_list():
		bomb_list = []
		for i in range(len(self._bombList)):
			bomb_pos = self._bombList[i].FindComponentByType("TransformGroup").GetPosition()
			bomb_pos = ()

		#shoot ball
		for i in range(len(self._bombList)):
			bompos = self._bombList[i].FindComponentByType("TransformGroup").GetPosition()
			self._bombList[i].FindComponentByType("TransformGroup").SetPosition(bompos + self._bomb_dirList[i])

		#check collision
		for i in range(len(self._bombList)):
			if(Getdistance(self._bombList[i].FindComponentByType("TransformGroup").GetPosition(), self.enemy.FindComponentByType("TransformGroup").GetPosition()) < self._distance):
				print("Collision!")		
'''