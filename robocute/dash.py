from loguru import logger

from crunge import yoga

from crunge.engine.overlay import Overlay

from crunge.engine.widget import Widget
#from crunge.engine.ui.flex import Row, Column

from robocute.vu import *
from robocute.node import *


class Drawer(Widget):
    def __init__(self, node=None):
        #self.node = node
        """
        style = yoga.StyleBuilder().size_percent(100, 100).flex_direction(
            yoga.FlexDirection.COLUMN
        ).build()
        """
        # style = yoga.Style()
        # style.set_flex_grow(0.25)
        # style.set_flex_shrink(0)

        # super().__init__(style=style, children=[node] if node else None)
        super().__init__(children=[node] if node else None)

        # self.add_child(node)

    """
    def _enable(self):
        super()._enable()
        self.add_child(self.node)
    """


class Dash(Overlay):
    def __init__(self, name):
        """
        style = yoga.StyleBuilder().size_percent(100, 100).flex_direction(
            yoga.FlexDirection.COLUMN
        ).build()
        """
        # style = yoga.Style()

        # super().__init__(name, style=style)
        super().__init__(name)

    def create_drawer(self, drawerName, node=None):
        drawer = Drawer(node)
        logger.debug(f"flex direction: {drawer.layout.layout_node.get_flex_direction()}")
        return drawer

    def draw_children(self):
        with Renderer.get_current().canvas_target() as canvas:
            super().draw_children()
