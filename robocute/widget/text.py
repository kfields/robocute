from crunge.engine.widget import Widget
from robocute.vu import TextVu

class Text(Widget):
    def __init__(self, text, fn=None):
        super().__init__()
        self.text = text
        self.fn = fn
        self.add_chip(TextVu())

    def process(self, event):
        if self.fn:
            self.fn()

