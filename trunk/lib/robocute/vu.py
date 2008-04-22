#import pyglet

import data

import pyglet
from pyglet import image

from base import *
from graphics import Graphics

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

class Vu(Base):
    def __init__(self, node):
        super(Vu, self).__init__()
        self.node = node
        self.width = 0
        self.height = 0
        self.hotspots = []
        #
        #query support
        self.hotHeight = 0
            
    '''
    Note: significant speed penalty for calling super.draw! ... super.anything for that matter.
    '''
    def draw(self, graphics):
        pass

    def batch(self, g):
        pass
    
    def add_hotspot(self, hotspot):
        self.hotspots.append(hotspot)
        
    def remove_hotspot(self, hotspot):
        self.hotspots.remove(hotspot)
        
    def has_hotspots(self):
        return len(self.hotspots) != 0
        
    def query(self, g):
        query = g.query        
        if(not query):
            return        
        if(not self.has_hotspots()): #temporary hack
            return
        pos = g.unproject(query.x, query.y)
        for hotspot in self.hotspots:
            hotX1 = g.x + hotspot.x
            hotY1 = g.y + hotspot.y
            hotX2 = hotX1 + hotspot.width
            hotY2 = hotY1 + hotspot.height
            if(pos[0] > hotX1 and pos[0] < hotX2):
                if(pos[1] > hotY1 and pos[1] < hotY2):
                    query.add_result(self.node, g.cellX, g.cellY, g.cellZ)
        
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
        super(TextVu, self).validate()
        self.width = self.text.width
        self.height = self.text.height
        
    def draw(self, graphics):
        #super(TextVu, self).draw(graphics)
        #either way works...
        #glPushMatrix()
        #glTranslatef(graphics.x, graphics.y, graphics.z)
        self.text.x = graphics.x
        self.text.y = graphics.y
        self.text.draw()
        #glPopMatrix()
        if graphics.query:
            self.query(graphics)        

class ImageVu(Vu):
    def __init__(self, node, imgSrc):
        super(ImageVu, self).__init__(node)
        self.imgSrc = imgSrc
        if(imgSrc != ''):
            self.image = load_image(imgSrc)
        else:
            self.image = None
        self.validate()
        self.add_hotspot(HotSpot(0,0,self.width,self.hotHeight))#fixme:put in base?
        
    def validate(self):
        super(ImageVu, self).validate()
        self.width = self.image.width
        self.height = self.image.height
        #query support
        self.hotHeight = self.height
        #hack?
        self.node.z = self.width
        
    def draw(self, graphics):
        #super(ImageVu, self).draw(graphics)
        if(self.image != None):
            self.image.blit(graphics.x, graphics.y, graphics.z)
        if graphics.query:
            self.query(graphics)            
