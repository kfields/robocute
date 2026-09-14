from loguru import logger

from crunge.engine.d2.view import SceneView2D
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.overlay import Overlay

from robocute.dash import Dash

class BubbleLayer(Overlay):
    def __init__(self, name):
        super().__init__(name)
        
class WidgetLayer(Overlay):
    def __init__(self, name):
        super().__init__(name)
        
class MouseLayer(Overlay):
    def __init__(self, name):
        super().__init__(name)

    '''
    def draw(self, graphics):
        g = graphics.copy() #fixme:necessary?
        for node in self.nodes:                
            vu = node.vu
            g.x = node.x
            g.y = node.y - vu.height #fixme:mouse.hotx & hoty!!!
            vu.draw(g)
    '''

class GameView(SceneView2D):
    def create_camera(self):
        self.camera = Camera2D()

    def _create(self):
        super()._create()
        self.bubbles = self.create_overlay('bubbles')
        #
        self.dash = self.create_overlay('dash')
        #
        self.widgets = self.create_overlay('widgets')
        #
        self.mice = self.create_overlay('mice')
        #
        self.query = None

    def create_overlay(self, name):
        if name == 'bubbles' :
            overlay = BubbleLayer(name)
        elif name == 'dash':
            overlay = Dash(name)            
        elif name == 'widgets':
            overlay = WidgetLayer(name)
        elif name == 'mice':
            overlay = MouseLayer(name)
        self.add_overlay(overlay)
        return overlay
