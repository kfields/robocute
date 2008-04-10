
from node import Node
from vu import ImageVu
from message import *

class MouseQuery(object):
    def __init__(self, events):
        self.events = events
        self.result = []
        #cheat ... need to build rectangle from events...later?
        event = events[0]
        self.x = event.x
        self.y = event.y 
    
    def process(self):
        if(not self.result):
            return
        #another cheat?
         #get last result, highest z
        result = self.result[len(self.result)-1]
        result.process(self.events[len(self.events)-1])
        
class Mouse(Node):
    def __init__(self):
        super(Mouse, self).__init__()
        self.vu = ImageVu(self, 'Pointer-Standard.png')
        self.vu.clickable = False
        
class MouseMessage(Message):
    def __init__(self, x, y, button, modifiers):
        super(MouseMessage, self).__init__()
        self.x = x
        self.y = y
        self.button = button
        self.modifiers = modifiers
    
class MousePressed(MouseMessage):
    def __init__(self,  x, y, button, modifiers):
        super(MousePressed, self).__init__(x, y, button, modifiers)
