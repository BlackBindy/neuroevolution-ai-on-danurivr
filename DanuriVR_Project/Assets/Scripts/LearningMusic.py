class LearningMusic(Actor.Actor):
    def __init__(self):
        self.BackgroundSoundContainer = Container(0)
        
        return

    def OnCreate(self, uid):
        self.BackgroundSoundComponent = self.BackgroundSoundContainer.FindComponentByType("Sound")
        self.ThisContainer = Container(uid)
        self.EffectSoundComponent = Sound(self.ThisContainer.AddNewComponent("Sound"))
        self.BackgroundSoundComponent.PropSound.SetSoundFilePath("$project/Assets/Resources/Sounds/02 Title Screen.mp3");
        self.BackgroundSoundComponent.PropSound.SetEffect(0);
        #self.BackgroundSoundComponent.PropSound.SetRepeat(0);
        self.BackgroundSoundComponent.PropSound.SetVolume(10.0);
        self.BackgroundSoundComponent.Play();

        return 0 
    def OnDestroy(self):
        return 0 
    def OnEnable(self):
        return 0 
    def OnDisable(self):
        return 0 
    def Update(self):
        
        return 0

    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        return;