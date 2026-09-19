'''
from crunge.engine.d2.sized_node_2d import SizedNode2D
from robocute.vu import BubbleVu
   
class Bubble(SizedNode2D):
    def __init__(self, children):
        super().__init__(children)
        #style=yoga.StyleBuilder().size_percent(100, 100).margin(yoga.Edge.ALL, 5).build()
        #style=yoga.Style()
        #super().__init__(items, style=style)
        #self.add_chip(BubbleVu())

class DashBubble(Bubble):
    def __init__(self, children):
        super().__init__(children)

class SpeechBubble(Bubble):
    def __init__(self, children):
        super().__init__(children)



'''
from crunge.engine.widget import Widget
from crunge import yoga

from robocute.node import *
from robocute.vu import BubbleVu
   
class Bubble(Widget):
    def __init__(self, children):
        #super().__init__(items)
        #style=yoga.StyleBuilder().size_percent(100, 100).margin(yoga.Edge.ALL, 5).build()
        super().__init__(children=children)
        #self.add_chip(BubbleVu())

class DashBubble(Bubble):
    def __init__(self, children):
        super().__init__(children)

class SpeechBubble(Bubble):
    def __init__(self, children):
        super().__init__(children)
