from loguru import logger

from crunge import yoga
from crunge.engine.overlay import Overlay
from robocute.widget import GameWidget

from robocute.vu import *
from robocute.node import *

class Drawer(GameWidget):
    def __init__(self, node = None):
        self.node = node
        '''
        style = yoga.StyleBuilder().size_percent(100, 100).flex_direction(
            yoga.FlexDirection.COLUMN
        ).build()
        '''
        style = yoga.Style()
        #style.set_flex_grow(0.25)
        #style.set_flex_shrink(0)

        super().__init__(style=style)

        #self.add_child(node)

    def _enable(self):
        super()._enable()
        self.add_child(self.node)

    def on_layout(self):
        super().on_layout()
        logger.debug(f"Drawer layout updated: {self.size}")

class Dash(Overlay):
    def __init__(self, name):
        '''
        style = yoga.StyleBuilder().size_percent(100, 100).flex_direction(
            yoga.FlexDirection.COLUMN
        ).build()
        '''
        style = yoga.Style()

        super().__init__(name, style=style)

    def on_layout(self):
        super().on_layout()
        logger.debug(f"Dash layout updated: {self.size}")
        logger.debug(f"drawer yoga children: {self.layout.get_child_count()}")

    def create_drawer(self, drawerName, node = None):
        drawer = Drawer(node)
        return drawer
        

    def draw_children(self):
        with Renderer.get_current().canvas_target() as canvas:
            super().draw_children()
