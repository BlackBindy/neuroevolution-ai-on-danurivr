class DanuriBombCon(Actor.Actor):
	def __init__(self):
		self.danuri_bomb_list = []
		return

	def OnCreate(self, uid):
		#print(uid)
        #self.UID = uid
		#print(self.container)
		return 0

	def Update(self):
		for bomb in self.danuri_bomb_list:
			obj = bomb[0]
			direction = bomb[1]

			pos = obj.FindComponentByType("TransformGroup").GetPosition()
			obj.FindComponentByType("TransformGroup").SetPosition(pos + direction)

	def AddDanuriBomb(self, container, pos, direction):
		new_bomb = container.LoadPrefab("$project/Assets/Bomb.prefab")
		new_bomb.PropInstance.SetShow(True)
		new_bomb.FindComponentByType("TransformGroup").SetPosition(pos + 0.5 * direction)
		self.danuri_bomb_list.append((new_bomb, direction))
