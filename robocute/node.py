
from crunge.engine.d2 import Node2D
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader

from robocute.base import *
from robocute.vu import *

class AbstractNode(Node2D):
    def __init__(self, dna = None, fn = None):
        super().__init__()
        self.dna = dna
        self.name = 'Unknown'
        self.fn = fn #not sure about this...

    def invalidate(self, flag = 1):
        pass
        
    def validate(self):
        pass
    
    #events
    def process(self, event):
        if(self.fn):
            self.fn(self)
        
class Node(AbstractNode):
    def __init__(self, dna = None, fn = None):
        super().__init__(dna, fn)
        #self.x = 0
        #self.y = 0
        #self.z = 0
        self.brain = None

    def register(self, app, coord = None):
        #pass
        self.validate()
 
    def validate(self):
        super().validate()
        
    def set_transform(self, transform):
        self.x = transform.x
        self.y = transform.y

    def get_transform(self):
        return Transform(self.x, self.y)        
'''
Text Node
'''
class Text(Node):
    def __init__(self, text, fn = None):
        super().__init__(fn)
        self.text = text
        self.fn = fn
        self.add(TextVu(self))
    def process(self, event):
        if(self.fn):
            fn()

sprite_loader = SpriteLoader()

'''
Image Node
'''
class Image(Node2D):
    def __init__(self, imgSrc, fn = None):
        super().__init__()
        self.model = sprite_loader.load("${resources}/image/" + imgSrc)
        self.fn = fn
