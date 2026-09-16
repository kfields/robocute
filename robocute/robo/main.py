
from robocute.robo import *
from robocute.robo.player import *
from robocute.robo.designer import * 

from ..builder import Dna

class AbstractDesigner(Robo):
    groupable = False
    def __init__(self, dna = None):
        super().__init__(dna)
        self.block_height = 0
        #self.vu = self.add(RoboVu('Selector.png'))
        '''
        if dna.img_src:
            self.vu = self.add(RoboVu(dna.img_src))
        '''
        #self.vu.hotspots = [] #clear the list

class DesignerClone(AbstractDesigner):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(DesignerCloneBrain())
        
class Designer(AbstractDesigner):
    def __init__(self, dna: Dna = None):
        self.dna.img_src = 'Selector.png'
        super().__init__(dna)
        self.brain = self.add(DesignerBrain())
        
    def clone(self, app, coord):
        clone = DesignerClone()
        clone.register(app, coord)
        return clone
        
class RoboCute(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain())
        #self.vu = self.add(RoboVu('robocute.png'))
        
class RoboBoy(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain())
        #self.vu = self.add(RoboVu('Character Boy.png'))
        
class RoboCatGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain())
        #self.vu = self.add(RoboVu('Character Cat Girl.png'))
        
class RoboHornGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain())
        #self.vu = self.add(RoboVu('Character Horn Girl.png'))
        
class RoboPinkGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain())
        #self.vu = self.add(RoboVu('Character Pink Girl.png'))
        
class RoboPrincessGirl(Robo):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add(PlayerBrain())
        #self.vu = self.add(RoboVu('Character Princess Girl.png'))