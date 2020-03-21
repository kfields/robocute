import pyglet
from pyglet.gl import *

from robocute.node import *
from robocute.vu import *
from robocute.shape import Rect

class WidgetVu(Vu):
    def __init__(self, node):
        super().__init__(node)
        #
        self.content = Rect()        
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
        super().validate()
        if not self.skin:
            return
        #else        
        self.skin.validate()
        #
        self.margin_left = self.skin.margin_left
        self.margin_right = self.skin.margin_right
        self.width = self.content.width + self.margin_left + self.margin_right
        #
        self.margin_top = self.skin.margin_top
        self.margin_bottom = self.skin.margin_bottom
        self.height = self.content.height + self.margin_bottom + self.margin_top
        
    def draw(self, graphics):
        super().draw(graphics)
        if not self.skin:
            return
        #else
        g = graphics.copy()
        g.width = self.width
        g.height = self.height
        self.skin.draw(g)

class Widget(Node):
    def __init__(self, items = None):
        self.items = items

    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, item):
        self.items.remove(item)                