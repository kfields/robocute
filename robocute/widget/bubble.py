from robocute.node import *
from robocute.widget import *
from robocute.vu import BubbleVu
   
class Bubble(GameWidget):
    def __init__(self, items):
        #super().__init__(items)
        #style=yoga.StyleBuilder().size_percent(100, 100).margin(yoga.Edge.ALL, 5).build()
        style=yoga.Style()
        super().__init__(items, style=style)
        #self.add(BubbleVu())

class DashBubble(Bubble):
    def __init__(self, items):
        super().__init__(items)

class SpeechBubble(Bubble):
    def __init__(self, items):
        super().__init__(items)


