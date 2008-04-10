
from robocute.bot.bot import *
from robocute.vu import *
from brain import Brain
from playerbrain import PlayerBrain

#was going to name it bot ... robo goes with the theme
    
class RoboVu(ImageVu):
    def __init__(self, node, imgSrc):
        super(RoboVu, self).__init__(node, imgSrc)
    def get_stack_height(self):
        return 100 #necessary for SpeechBubble!
        
class Robo(Bot):
    def __init__(self):
        super(Robo, self).__init__()
'''
'''
Avatar_singleton = None
class Avatar(Robo):
    def __new__(cls, *args, **kargs):
        global Avatar_singleton
        if not Avatar_singleton:
            #obj = object.__new__(cls)
            obj = RoboBoy()
            #obj = RoboCute()
            Avatar_singleton = obj
            obj.__init__(*args, **kargs)
        return Avatar_singleton
    def __init__(self):
        super(Avatar, self).__init__()

class RoboCute(Robo):
    def __init__(self):
        super(RoboCute, self).__init__()
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'robocute.png')
        
class RoboBoy(Robo):
    def __init__(self):
        super(RoboBoy, self).__init__()
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'Character Boy.png')
        
class RoboCatGirl(Robo):
    def __init__(self):
        super(RoboCatGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Cat Girl.png')
        
class RoboHornGirl(Robo):
    def __init__(self):
        super(RoboHornGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Horn Girl.png')
        
class RoboPinkGirl(Robo):
    def __init__(self):
        super(RoboPinkGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Pink Girl.png')
        
class RoboPrincessGirl(Robo):
    def __init__(self):
        super(RoboPrincessGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Princess Girl.png')