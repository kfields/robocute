from loguru import logger

from crunge import sdl
from crunge import yoga
from crunge.engine.ui import Widget

from robocute.node import *
from robocute.vu import *
from robocute.shape import Rect


class GameWidget(Widget):
    def __init__(self, children=[], style=None):
        super().__init__(style=style)
        for child in children:
            self.add_child(child)


"""
Text Node
"""


class Text(GameWidget):
    def __init__(self, text, fn=None):
        super().__init__(fn)
        self.text = text
        self.fn = fn
        self.add(TextVu(self))

    def process(self, event):
        if self.fn:
            fn()

"""
Image Node
"""


class Image(GameWidget):
    def __init__(self, imgSrc, fn=None):
        style = yoga.StyleBuilder().height(50).margin(yoga.Edge.ALL, 5).build()
        super().__init__(style=style)
        self.fn = fn
        self.add(ImageVu(imgSrc))

    def on_layout(self):
        super().on_layout()
        logger.debug(f"Image layout position: {self.global_position}, size: {self.size}")

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        if event.button == 1 and event.down: # Left mouse button
            x, y = event.x, event.y
            if self.hit_test(x, y):
                self.fn(self)
                return True # Indicate that the event was handled
