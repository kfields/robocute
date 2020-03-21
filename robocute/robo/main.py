
from robocute.robo import *
import robocute.robo.brain
from robocute.robo.player import *
from robocute.robo.designer import * 

class AbstractDesigner(Robo):
    groupable = False
    def __init__(self, dna = None):
        super().__init__(dna)
        self.height = 0
        self.vu = RoboVu(self, 'Selector.png')
        self.vu.hotspots = [] #clear the list

class DesignerClone(AbstractDesigner):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = DesignerCloneBrain(self)
        
class Designer(AbstractDesigner):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = DesignerBrain(self)
        
    def clone(self, app, coord):
        clone = DesignerClone()
        clone.register(app, coord)
        return clone
        
class RoboCute(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'robocute.png')
        
class RoboBoy(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = PlayerBrain(self)
        self.vu = RoboVu(self, 'Character Boy.png')
        
class RoboCatGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vu = RoboVu(self, 'Character Cat Girl.png')
        
class RoboHornGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vu = RoboVu(self, 'Character Horn Girl.png')
        
class RoboPinkGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vu = RoboVu(self, 'Character Pink Girl.png')
        
class RoboPrincessGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vu = RoboVu(self, 'Character Princess Girl.png')