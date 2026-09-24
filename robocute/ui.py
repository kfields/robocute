from loguru import logger

from crunge import yoga

from crunge.engine.ui.ui_overlay import UiOverlay

from crunge.engine.widget import Widget

from robocute.vu import *
from robocute.node import *


class Drawer(Widget):
    def __init__(self, node=None):
        super().__init__(children=[node] if node else None)


class Ui(UiOverlay):
    def __init__(self, name):
        super().__init__(name)

    def create_drawer(self, drawerName, node=None):
        drawer = Drawer(node)
        logger.debug(f"flex direction: {drawer.layout.layout_node.get_flex_direction()}")
        return drawer
