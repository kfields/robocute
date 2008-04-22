
from robocute.bot.bot import *
from robocute.vu import *
from brain import Brain
from player import *
from designer import *

#was going to name it bot ... robo goes with the theme
    
class RoboVu(BotVu):
    def __init__(self, node, imgSrc):
        super(RoboVu, self).__init__(node, imgSrc)
        
class Robo(Bot):
    def __init__(self):
        super(Robo, self).__init__()

class AbstractDesigner(Robo):
    groupable = False
    def __init__(self):
        super(AbstractDesigner, self).__init__()
        self.height = 0
        self.vu = RoboVu(self, 'Selector.png')
        self.vu.hotspots = [] #clear the list

class DesignerClone(AbstractDesigner):
    def __init__(self):
        super(DesignerClone, self).__init__()
        self.brain = DesignerCloneBrain(self)
        
class Designer(AbstractDesigner):
    def __init__(self):
        super(Designer, self).__init__()
        self.brain = DesignerBrain(self)
        
    def clone(self, app, coord):
        clone = DesignerClone()
        clone.register(app, coord)
        return clone
        
class RoboCute(Robo):
    def __init__(self):
        super(RoboCute, self).__init__()
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'robocute.png')
        
class CharacterBoy(Robo):
    def __init__(self):
        super(CharacterBoy, self).__init__()
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'Character Boy.png')
        
class CharacterCatGirl(Robo):
    def __init__(self):
        super(CharacterCatGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Cat Girl.png')
        
class CharacterHornGirl(Robo):
    def __init__(self):
        super(CharacterHornGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Horn Girl.png')
        
class CharacterPinkGirl(Robo):
    def __init__(self):
        super(CharacterPinkGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Pink Girl.png')
        
class CharacterPrincessGirl(Robo):
    def __init__(self):
        super(CharacterPrincessGirl, self).__init__()
        self.vu = RoboVu(self, 'Character Princess Girl.png')