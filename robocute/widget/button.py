
import pyglet
from pyglet.gl import *

from robocute.node import *
from robocute.widget import *
from robocute.skin import *
   
'''
Bubble
'''
class ButtonVu(WidgetVu):
    def __init__(self, node, slicesName):
        super().__init__(node)        
        self.skin = HorizontalSkin(FileSkinData(slicesName, 3))

    def validate(self):
        self.content.height = self.skin.content.height
        self.content.width = 0
        for item in self.node.items:
            vu = item.vu
            vu.validate()
            self.content.width += vu.width
        
        super().validate()

    def draw(self, graphics):
        super().draw(graphics)
        self.draw_items(graphics)
            
    def draw_items(self, graphics):
        g = graphics.copy()
        g.x += self.margin_left
        g.y += self.margin_bottom
        gY = g.y
        
        for item in self.node.items:
            vu = item.vu
            g.y = gY + (self.content.height * .5) - (vu.height * .5) #just center everything for now
            vu.draw(g)
            g.x += vu.width + self.hspace
                
class AbstractButton(Widget):
    def __init__(self, items):
        super().__init__(items)

class Button(Button):
    def __init__(self, items):
        super().__init__(items)
        self.vu = ButtonVu(self, 'DashButton')
        self.vu.validate() #necessary evil. :)
