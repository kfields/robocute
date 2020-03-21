
import pyglet

import robocute

from robocute.widget import *
from robocute.skin import *

'''
DocVu
'''
class DocVu(WidgetVu):
    def __init__(self, node, slicesName):
        super().__init__(node)        
        self.skin = GridSkin(GridSkinner(slicesName))
        #
    def validate(self):
        #self.content.width = 0
        self.content.width = 240        
        #self.content.height = self.skin.content.height
        self.content.height = 320
        '''
        for item in self.node.items:
            vu = item.vu
            vu.validate()
            self.content.width += vu.width
        '''
        doc = self.node.document
        docWidth = self.content.width
        docHeight = self.content.height
        self.layout = pyglet.text.layout.TextLayout(doc, docWidth, docHeight, True)        
        #self.layout = pyglet.text.layout.ScrollableTextLayout(doc, docWidth, docHeight, True)
        #self.layout = pyglet.text.layout.IncrementalTextLayout(doc, docWidth, docHeight, True)
        #self.layout.view_x = 32
        #self.layout.view_y = 32        
        super().validate()
        self.on_resize(0, 0)

    def on_resize(self, width, height):
        #super().on_resize(width, height)
        self.layout.begin_update()
        self.layout.x = self.margin_left
        #self.layout.y = self.margin_bottom
        if self.layout.content_height < self.content.height:
            self.layout.y = self.margin_bottom + self.content.height - self.layout.content_height
        else:
            self.layout.y = self.margin_bottom
            
        self.layout.width = self.content.width
        self.layout.height = self.content.height 
        self.layout.end_update()

    def draw(self, graphics):
        super().draw(graphics)
        self.layout.draw()
            
'''
DocWidget
'''                
class DocWidget(Widget):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        #
        print(pyglet.resource.get_script_home())
        self.document = pyglet.text.load(filename)
        #
        self.vu = DocVu(self, 'HelpBubble')
        self.vu.validate() #necessary evil. :)  
