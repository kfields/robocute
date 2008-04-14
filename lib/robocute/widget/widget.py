import pyglet
from pyglet.gl import *

from robocute.node import *
from robocute.vu import *

class WidgetVu(Vu):
    def __init__(self, node):
        super(WidgetVu, self).__init__(node)
        #        
        self.margin_top = 5
        self.margin_bottom = 5        
        self.margin_left = 5
        self.margin_right = 5
        #
        self.hspace = 5
        self.vspace = 5
        #
        self.skin = None

    def validate(self):
        super(WidgetVu, self).validate()
        if not self.skin:
            return
        self.skin.validate()
        #else
        self.width = 0
        self.height = 0
        #
        self.margin_left = self.skin.margin_left
        #self.width += self.margin_left
        self.margin_right = self.skin.margin_right
        #self.width += self.margin_right
        self.width = self.skin.width
        #
        self.margin_top = self.skin.margin_top
        #self.height += self.margin_top 
        self.margin_bottom = self.skin.margin_bottom
        #self.height += self.margin_bottom
        self.height = self.skin.height
        
    def draw(self, graphics):
        super(WidgetVu, self).draw(graphics)
        if not self.skin:
            return
        #else
        g = graphics.copy()
        g.width = self.width
        g.height = self.height
        self.skin.draw(g)

class Widget(Node):
    def __init__(self):
        pass
        