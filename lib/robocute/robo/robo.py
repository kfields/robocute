
from robocute.node import *
from robocute.vu import *
from brain import Brain
from playerbrain import PlayerBrain

#was going to name it bot ... robo goes with the theme

class RoboVu(ImageVu):
    def __init__(self, node, imgSrc):
        super(RoboVu, self).__init__(node, imgSrc)
    def get_stack_height(self):
        return 100 #necessary for SpeechBubble!
        
class Robo(Node):
    def __init__(self):
        super(Robo, self).__init__()
        self.brain = None
        
class RoboBoy(Robo):
    def factory(cls, *args):
        return RoboBoy()
    
    def __init__(self):
        super(RoboBoy, self).__init__()
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'Character Boy.png')
        
class RoboCatGirl(Robo):
    def factory(cls, *args):
        return RoboCatGirl()
    
    def __init__(self):
        super(RoboCatGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Cat Girl.png')
        
class RoboHornGirl(Robo):
    def factory(cls, *args):
        return RoboHornGirl()
    
    def __init__(self):
        super(RoboHornGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Horn Girl.png')
        
class RoboPinkGirl(Robo):
    def factory(cls, *args):
        return RoboPinkGirl()
    
    def __init__(self):
        super(RoboPinkGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Pink Girl.png')
        
class RoboPrincessGirl(Robo):
    def factory(cls, *args):
        return RoboPrincessGirl()
    
    def __init__(self):
        super(RoboPrincessGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Princess Girl.png')