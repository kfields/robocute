from crunge.engine.widget import Widget
from crunge import yoga
from crunge import sdl
from robocute.vu import ImageVu

class Image(Widget):
    def __init__(self, img_src, fn=None):
        style = yoga.StyleBuilder().height(50).margin(yoga.Edge.ALL, 5).build()
        super().__init__(style=style)
        self.fn = fn
        self.add_chip(ImageVu(img_src))

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        if event.button == 1 and event.down: # Left mouse button
            x, y = event.x, event.y
            if self.hit_test(x, y):
                self.fn(self)
                return True # Indicate that the event was handled
