from robocute.robo import Robo
from robocute.robo.designer_brain import * 

from ..builder import Dna

class BaseDesigner(Robo):
    groupable = False
    def __init__(self, dna = None):
        super().__init__(dna)
        self.block_height = 0

class DesignerClone(BaseDesigner):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = self.add_chip(DesignerCloneBrain())
        
class Designer(BaseDesigner):
    def __init__(self, dna: Dna = None):
        self.dna.img_src = 'Selector.png'
        super().__init__(dna)
        self.brain = self.add_chip(DesignerBrain())
        
    def clone(self, app, coord):
        clone = DesignerClone()
        clone.register(app, coord)
        return clone
