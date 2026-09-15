
from robocute.robo import *
import robocute.robo.brain
from robocute.robo.player import *
from robocute.robo.designer import * 

class AbstractDesigner(Robo):
    groupable = False
    def __init__(self, dna = None):
        super().__init__(dna)
        #self.height = 0
        self.vu = RoboVu('Selector.png')
        self.vu.hotspots = [] #clear the list

class DesignerClone(AbstractDesigner):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(DesignerCloneBrain())
        
class Designer(AbstractDesigner):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(DesignerBrain())
        
    def clone(self, app, coord):
        clone = DesignerClone()
        clone.register(app, coord)
        return clone
        
class RoboCute(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain(self))
        self.vu = RoboVu('robocute.png')
        
class RoboBoy(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain(self))
        self.vu = RoboVu('Character Boy.png')
        
class RoboCatGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain(self))
        self.vu = RoboVu('Character Cat Girl.png')
        
class RoboHornGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain(self))
        self.vu = RoboVu('Character Horn Girl.png')
        
class RoboPinkGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain(self))
        self.vu = RoboVu('Character Pink Girl.png')
        
class RoboPrincessGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain(self))
        self.vu = RoboVu('Character Princess Girl.png')