
from robocute.robo import *
import brain
from player import *
from designer import * 

class AbstractDesigner(Robo):
    groupable = False
    def __init__(self, dna = None):
        super(AbstractDesigner, self).__init__(dna)
        self.height = 0
        self.vu = RoboVu(self, 'Selector.png')
        self.vu.hotspots = [] #clear the list

class DesignerClone(AbstractDesigner):
    def __init__(self, dna = None):
        super(DesignerClone, self).__init__(dna)
        self.brain = DesignerCloneBrain(self)
        
class Designer(AbstractDesigner):
    def __init__(self, dna = None):
        super(Designer, self).__init__(dna)
        self.brain = DesignerBrain(self)
        
    def clone(self, app, coord):
        clone = DesignerClone()
        clone.register(app, coord)
        return clone
        
class RoboCute(Robo):
    def __init__(self, dna = None):
        super(RoboCute, self).__init__(dna)
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'robocute.png')
        
class CharacterBoy(Robo):
    def __init__(self, dna = None):
        super(CharacterBoy, self).__init__(dna)
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'Character Boy.png')
        
class CharacterCatGirl(Robo):
    def __init__(self, dna = None):
        super(CharacterCatGirl, self).__init__(dna)
        self.vu = RoboVu(self, 'Character Cat Girl.png')
        
class CharacterHornGirl(Robo):
    def __init__(self, dna = None):
        super(CharacterHornGirl, self).__init__(dna)
        self.vu = RoboVu(self, 'Character Horn Girl.png')
        
class CharacterPinkGirl(Robo):
    def __init__(self, dna = None):
        super(CharacterPinkGirl, self).__init__(dna)
        self.vu = RoboVu(self, 'Character Pink Girl.png')
        
class CharacterPrincessGirl(Robo):
    def __init__(self, dna = None):
        super(CharacterPrincessGirl, self).__init__(dna)
        self.vu = RoboVu(self, 'Character Princess Girl.png')