
import copy

'''
This file is the bottom of the import heirarchy so I'm gonna stick fundamentals in here for now.
'''

'''
Block Coordinates
'''
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

'''
2D position and rotation
'''
class Transform:
    def __init__(self, x, y, r=0):
        self.x = x
        self.y = y
        self.r = r
        
    def copy(self):
        return copy.copy(self)

from vu import *
from brain import Brain

    
class AbstractCell(list):
    def __init__(self):
        pass
        
class AbstractNode(object):
    def __init__(self, fn = None):
        self.name = 'Unknown'
        self.vu = None
        self.fn = fn #not sure about this...
    #
    def copy(self):
        return copy.copy(self)
    def deep_copy(self):
        return copy.deepcopy(self)
    #   
    def set_vu(self, vu):
        self.vu = vu
    def get_vu(self):
        return self.vu
    def register(self, scene, coord):
        pass
    def has_vacancy(self):
        return False
    #events
    def process(self, event):
        if(self.fn):
            self.fn(self)
        print self, event
        
class Node(AbstractNode):
    def __init__(self, fn = None):
        super(Node, self).__init__(fn)
        self.x = 0
        self.y = 0
        self.z = 0
        self.brain = None
    def set_transform(self, transform):
        self.x = transform.x
        self.y = transform.y
    def get_transform(self):
        return Transform(self.x, self.y)
    def get_brain(self):
        return self.brain
    def register(self, scene, coord):
        if(self.brain != None):
            self.brain.set_scene(scene)
            self.brain.set_coord(coord)
        if self.vu:
            self.vu.validate() #fixme:ugh ...
        
    
'''
Text Node
'''
class Text(Node):
    def __init__(self, text, fn = None):
        super(Text, self).__init__(fn)
        self.text = text
        self.fn = fn
        self.vu = TextVu(self)
    def process(self, event):
        if(self.fn):
            fn()
'''
Image Node
'''
class Image(Node):
    def __init__(self, imgSrc, fn = None):
        super(Image, self).__init__(fn)
        self.imgSrc = imgSrc
        self.fn = fn
        self.vu = ImageVu(self, imgSrc)
'''
Button Node
'''
class Button(Node):
    def __init__(self):
        super(Button, self).__init__()
