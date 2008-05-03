
from base import *
from vu import *
#import brain

class AbstractNode(Base):
    def __init__(self, dna = None, fn = None):
        super(AbstractNode, self).__init__(dna)
        self.name = 'Unknown'
        self.vu = None
        self.fn = fn #not sure about this...

    def delete(self):
        if self.vu:
            self.vu.delete()
        super(AbstractNode, self).delete()
                
    def register(self, app, coord = None):
        super(AbstractNode, self).register(app, coord)
        if self.vu:
            self.vu.register(app, coord)

    def invalidate(self, flag = 1):
        super(AbstractNode, self).invalidate(flag)
        if self.vu:
            self.vu.invalidate(flag)        
                
    def validate(self):
        super(AbstractNode, self).validate()
        if self.vu:
            self.vu.validate()        
    
    #events
    def process(self, event):
        if(self.fn):
            self.fn(self)
        
class Node(AbstractNode):
    def __init__(self, dna = None, fn = None):
        super(Node, self).__init__(dna, fn)
        self.x = 0
        self.y = 0
        self.z = 0
        self.brain = None

    def delete(self):
        if self.brain:
            self.brain.delete()
        super(Node, self).delete()

    def register(self, app, coord = None):
        super(Node, self).register(app, coord)
        if self.brain:
            self.brain.register(app, coord)
        
    def validate(self):
        super(Node, self).validate()
        
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
