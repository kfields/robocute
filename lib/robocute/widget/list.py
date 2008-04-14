
import pyglet
from pyglet.gl import *

from robocute.node import *
from robocute.vu import *
   
'''
Bubble
'''
class ListVu(Vu):
    def __init__(self, node, imgName):
        super(ListVu, self).__init__(node)
        self.image = [None] * 3
        self.width = 0
        self.height = 0
        self.vspace = 5
        self.margin_top = 5
        self.margin_bottom = 5        
        self.margin_left = 5
        self.margin_right = 5
        
        if(imgName == ''):
            self.image = None
            return
        #else
        imgCount = 0
        
        while(imgCount != 3):
            self.image[imgCount] = load_image(imgName + '_0' + str(imgCount+1) + '.png')
            imgCount += 1
        #
        self.validate()

    def validate(self):
        self.height = 0
        self.width = self.image[0].width
        #
        self.margin_top = self.image[0].height
        self.height += self.margin_top 
        self.margin_bottom = self.image[2].height
        self.height += self.margin_bottom
        #
        #fixme:need spacer on end...
        for item in self.node.items:
            vu = item.vu
            vu.validate()
            self.height += vu.height
        #
        self.height += self.vspace * len(self.node.items)

    def draw(self, graphics):
        if(self.image == None):
            return
        #else
        #bottom slice
        self.image[0].blit(graphics.x, graphics.y, graphics.z)
        graphics.y += self.margin_bottom        
        #middle slice
        scissor = graphics.project(graphics.x, graphics.y)
        scissorX = GLint(int(scissor[0])) #only way!!!
        scissorY = GLint(int(scissor[1]))
        scissorW = self.width
        #scissorH = self.height - self.margin_top + 1
        scissorH = self.height + self.margin_top + 1
        glEnable(GL_SCISSOR_TEST)
        glScissor(scissorX, scissorY, scissorW, scissorH)
        #
        blitTop = graphics.y + self.height
        while(graphics.y <= blitTop ):
            self.image[1].blit(graphics.x, graphics.y, graphics.z)
            graphics.y += self.image[1].height
        #
        glDisable(GL_SCISSOR_TEST)
        #end slice
        self.image[2].blit(graphics.x, graphics.y, graphics.z)
        
        graphics.y = 0
        self.draw_items(graphics)
            
    def draw_items(self, graphics):
        g = graphics.copy()
        #g.height = self.height
        g.width = self.width
        #g.x += self.margin_left
        g.y += self.margin_bottom
        
        gX = g.x
        gY = g.y
        for item in reversed(self.node.items):
            vu = item.vu
            #g.y = gY + (g.height * .5) - (vu.height * .5) #just center everything for now
            g.x = gX + (g.width * .5) - (vu.width * .5) #just center everything for now
            vu.draw(g)
            #g.x += vu.width + 5 #fixme:self.spacer?
            g.y += vu.height + self.vspace #fixme:self.spacer?
            
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    #2.5D support
    def get_stack_height(self):
        return self.height

class List(Node):
    def __init__(self, items):
        super(List, self).__init__()
        self.items = items

    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, item):
        self.items.remove(item)        