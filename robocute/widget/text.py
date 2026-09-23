from crunge.engine.ui import Text as CrungeText
#from robocute.vu import TextVu


class Text(CrungeText):
    def __init__(self, text, fn=None):
        super().__init__(text)
        self.text = text
        self.fn = fn

    def process(self, event):
        if self.fn:
            self.fn()
