class LoadGameScene(Actor.Actor):
	def __init__(self):
		return

	def OnCreate(self, uid):
		return 0

	def Update(self):
		return 0

	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		if (msg == "Button_OnClick") :
			result = GetWorldContainer().FindComponentByType("World").LoadScene("$project/Assets/main.fsf");
			print(result)