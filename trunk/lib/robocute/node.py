
#import copy

from vu import *
from brain import Brain

class AbstractNode(object):
    def __init__(self, fn = None):
        self.name = 'Unknown'
        self.vu = None
        self.fn = fn #not sure about this...
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
            self.fn()
        print self, event
        
class NilNode(AbstractNode):
    def __init__(self):
        super(NilNode, self).__init__()

class Node(AbstractNode):
    def __init__(self, fn = None):
        super(Node, self).__init__(fn)
        self.transform = (0, 0, 0) #just use tuples for now.
        self.brain = None
    def set_transform(self, transform):
        self.transform = transform
    def get_transform(self):
        return self.transform
    def get_brain(self):
        return self.brain
    def register(self, scene, coord):
        if(self.brain != None):
            self.brain.set_scene(scene)
            self.brain.set_coord(coord)
    
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
