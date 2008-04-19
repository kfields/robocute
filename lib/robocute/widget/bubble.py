
import pyglet
from pyglet.gl import *

from robocute.node import *
from robocute.widget.widget import *
from robocute.widget.skin import *
   
'''
Bubble
'''
class BubbleVu(WidgetVu):
    def __init__(self, node, slicesName):
        super(BubbleVu, self).__init__(node)        
        self.skin = HorizontalSkin(slicesName)

    def validate(self):
        super(BubbleVu, self).validate()
        self.height = self.skin.height
        for item in self.node.items:
            vu = item.vu
            vu.validate()
            self.width += vu.width

    def draw(self, graphics):
        super(BubbleVu, self).draw(graphics)
        self.draw_items(graphics)
            
    def draw_items(self, graphics):
        g = graphics.copy()
        g.height = self.height
        g.x += self.margin_left
        g.y += self.margin_bottom
        gY = g.y
        
        for item in self.node.items:
            vu = item.vu
            g.y = gY + (g.height * .5) - (vu.height * .5) #just center everything for now
            vu.draw(g)
            g.x += vu.width + self.hspace
                
    #2.5D support
    #def get_stack_height(self):
    #    return self.height

class Bubble(Node):
    def __init__(self, items):
        super(Bubble, self).__init__()
        self.items = items

class DashBubble(Bubble):
    def __init__(self, items):
        super(DashBubble, self).__init__(items)
        self.vu = BubbleVu(self, 'DashBubble')
        self.vu.validate() #necessary evil. :)

class SpeechBubble(Bubble):
    def __init__(self, items):
        super(SpeechBubble, self).__init__(items)
        self.vu = BubbleVu(self, 'SpeechBubble')
        self.vu.validate()


