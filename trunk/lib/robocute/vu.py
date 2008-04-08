#import pyglet

import data

from graphics import *

from pyglet import image


def load_image(filename):
    return image.load(data.filepath('image/' + filename))

class Vu(object):    
    def __init__(self, node):
        self.node = node
        self.width = 0
        self.height = 0
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
        ft = pyglet.font.load('Verdana', 14)
        self.text = pyglet.font.Text(ft, self.node.text)
        self.text.color=(0,0,0,1)#red
        self.text.valign='center'
        self.validate()
        
    def validate(self):
        self.width = self.text.width
        self.height = self.text.height

    def draw(self, graphics):
        #either way works...
        #glPushMatrix()
        #glTranslatef(graphics.x, graphics.y, graphics.z)
        self.text.x = graphics.x
        self.text.y = graphics.y
        self.text.draw()
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
        #hack?
        self.node.z = self.width
        
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