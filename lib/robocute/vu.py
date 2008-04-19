#import pyglet

import data

import pyglet
from pyglet import image

from graphics import Graphics
from mesh import Mesh

'''
HotSpot : Just a way to clip events right now.  More in the future.
'''
class HotSpot():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y        
        self.width = width
        self.height = height
        
def load_image(filename):
    return image.load(data.filepath('image/' + filename))

class Vu(object):
    def __init__(self, node):
        self.node = node
        self.width = 0
        self.height = 0
        self.hotspots = []
        self.valid = False
        #
        #2.5D support        
        self.stack_height = 0
        
    def validate(self):
        self.valid = True
        
    def draw(self, graphics):
        pass

    def visit(self, vu):
        pass
    
    def add_hotspot(self, hotspot):
        self.hotspots.append(hotspot)
        
    def remove_hotspot(self, hotspot):
        self.hotspots.remove(hotspot)
        
    def has_hotspots(self):
        return len(self.hotspots) != 0
        
class TextVu(Vu):
    def __init__(self, node):
        super(TextVu, self).__init__(node)
        ft = pyglet.font.load('Verdana', 14)
        self.text = pyglet.font.Text(ft, self.node.text)
        self.text.color=(0,0,0,1)#red
        self.text.valign='center'
        self.validate()
        self.add_hotspot(HotSpot(0,0,self.width,self.height))#fixme:put in base?
        
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
        self.add_hotspot(HotSpot(0,0,self.width,self.height))#fixme:put in base?
        
    def validate(self):
        self.width = self.image.width
        self.height = self.image.height
        #2.5D support
        self.stack_height = self.height
        #hack?
        self.node.z = self.width
        
    def draw(self, graphics):
        if(self.image != None):
            self.image.blit(graphics.x, graphics.y, graphics.z)
        graphics.visit(self) #needs to be in Vu?

class MeshImageVu(ImageVu):
    def __init__(self, node, imgSrc):
        super(MeshImageVu, self).__init__(node, imgSrc)
        self.mesh = Mesh()
        self.mesh.from_image(self.image)
        
    def draw(self, graphics):
        self.mesh.draw(graphics)
        graphics.visit(self) #needs to be in Vu?