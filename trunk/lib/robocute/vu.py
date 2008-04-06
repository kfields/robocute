#import pyglet

import data

from graphics import *

from pyglet import image


def load_image(filename):
    return image.load(data.filepath('image/' + filename))

class Vu(object):    
    def __init__(self, node):
        self.node = node
        self.clickable = True #better name?
    def draw(self, graphics):
        pass
    def get_height(self):
        return 0
    def get_width(self):
        return 0    
    #2.5D support
    def get_stack_height(self):
        return 0
    #event support
    def visit(self, vu):
        pass
        
class TextVu(Vu):
    def __init__(self, node):
        super(TextVu, self).__init__(node)
        self.label = pyglet.text.Label(self.node.text,
                          font_name='Verdana',
                          #font_size=16,
                          font_size=14,
                          color=(0,0,0, 255),
                          valign='center')
        self.validate()
        
    def validate(self):
        self.width = self.label.content_width
        self.height = self.label.content_height

    def draw(self, graphics):
        #either way works...
        #glPushMatrix()
        #glTranslatef(graphics.x, graphics.y, graphics.z)
        self.label.x = graphics.x
        self.label.y = graphics.y
        self.label.draw()
        if(graphics.query):
            graphics.visit(self)
        #glPopMatrix()

class ImageVu(Vu):
    def __init__(self, node, imgSrc):
        super(ImageVu, self).__init__(node)
        if(imgSrc != ''):
            self.image = load_image(imgSrc)
        else:
            self.image = None
        self.validate()
        
    def validate(self):
        self.width = self.image.width
        self.height = self.image.height
        
    def draw(self, graphics):
        if(self.image != None):
            self.image.blit(graphics.x, graphics.y, graphics.z)
        graphics.visit(self) #needs to be in Vu?
        
    def get_height(self):
        return self.image.height
    
    def get_width(self):
        return self.image.width
    
    #2.5D support
    def get_stack_height(self):
        return self.image.height