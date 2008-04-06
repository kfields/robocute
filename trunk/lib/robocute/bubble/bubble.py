
import pyglet
from pyglet.gl import *

from robocute.node import *
from robocute.vu import *
   
'''
Bubble
'''
class BubbleVu(Vu):
    def __init__(self, node, imgName):
        super(BubbleVu, self).__init__(node)
        self.image = [None] * 3
        self.width = 0
        self.height = 0
        #self.widths = None
        self.margin_left = 0
        self.margin_right = 0
        
        if(imgName == ''):
            self.image = None
            return
        #else
        self.image[0] = load_image(imgName + '_01.png')
        self.image[1] = load_image(imgName + '_02.png')
        self.image[2] = load_image(imgName + '_03.png')
        #
        self.validate()

    def validate(self):
        self.width = 0
        self.height = self.image[0].height
        #
        self.margin_left = self.image[0].width
        self.width += self.margin_left 
        self.margin_right = self.image[2].width
        self.width += self.margin_right
        #
        #fixme:need spacer on end...
        for item in self.node.items:
            vu = item.vu
            vu.validate()
            self.width += vu.width

    def draw(self, graphics):
        if(self.image == None):
            return
        #else
        #home slice
        self.image[0].blit(graphics.x, graphics.y, graphics.z)

        scissor = graphics.project(graphics.x + self.margin_left, graphics.y)
        #scissorX = GLint(int(scissor[0].value))
        scissorX = GLint(int(scissor[0])) #only way!!!
        #scissorY = GLint(int(scissor[1].value))
        scissorY = GLint(int(scissor[1]))

        scissorW = self.width - (self.margin_left + self.margin_right) + 1
        scissorH = self.height
        glEnable(GL_SCISSOR_TEST)
        glScissor(scissorX, scissorY, scissorW, scissorH)
        #
        blitX = graphics.x + self.margin_left
        while(blitX <= graphics.x + self.width):
            self.image[1].blit(blitX, graphics.y, graphics.z)
            blitX += self.image[1].width
        #
        glDisable(GL_SCISSOR_TEST)
        #end slice
        self.image[2].blit(graphics.x + self.width - self.margin_right, graphics.y, graphics.z)

        self.draw_items(graphics)
            
    def draw_items(self, graphics):
        g = graphics.copy()
        g.height = self.height
        g.x += self.margin_left

        gY = g.y
        for item in self.node.items:
            vu = item.vu
            h = vu.height
            g.y = gY + (g.height * .5) - (vu.height * .5) #just center everything for now
            vu.draw(g)
            g.x += vu.width + 5 #fixme:self.spacer?
            
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    #2.5D support
    def get_stack_height(self):
        return self.height

class Bubble(Node):
    def __init__(self, items):
        super(Bubble, self).__init__()
        self.items = items

class DashBubble(Bubble):
    def __init__(self, items):
        super(DashBubble, self).__init__(items)
        #self.brain = brain
        self.vu = BubbleVu(self, 'DashBubble')

class SpeechBubble(Bubble):
    def __init__(self, items):
        super(SpeechBubble, self).__init__(items)
        #self.brain = brain
        self.vu = BubbleVu(self, 'SpeechBubble')


