class SelectScene(Actor.Actor):
	def __init__(self):
		return

	def OnCreate(self, uid):
		return 0

	def Update(self):
		return 0

	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		if (msg == "Game_OnClick") :
			GetWorldContainer().FindComponentByType("World").LoadScene("$project/Assets/test.fsf");

		if (msg == "Simulation_OnClick") :
			GetWorldContainer().FindComponentByType("World").LoadScene("$project/Assets/test-learning.fsf");
