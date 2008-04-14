
from node import Node
from node import Coord
from vu import ImageVu
from message import *

class Result(Coord):
    def __init__(self, x, y, node):
        Coord.__init__(self, x, y)
        self.node = node
                
class MouseQuery(object):
    def __init__(self, events):
        self.events = events
        self.results = []
        #cheat ... need to build rectangle from events...later?
        event = events[0]
        self.x = event.x
        self.y = event.y 
        #now it's really getting nuts.
        self.cellX = 0
        self.cellY = 0
    
    def add_result(self, node):
        self.results.append(Result(self.cellX, self.cellY, node))
                            
    def process(self):
        if(not self.results):
            return
        #get last result, highest z
        result = self.results[len(self.results)-1]
        #result.process(self.events[len(self.events)-1])
        for event in self.events:
            result.node.process(event)
        
class Mouse(Node):
    def __init__(self):
        super(Mouse, self).__init__()
        self.vu = ImageVu(self, 'Pointer-Standard.png')
        #self.vu.clickable = False
        self.vu.hotspots = [] #clear the list
        
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

class MouseMoved(MouseMessage):
    def __init__(self,  x, y, button, modifiers):
        super(MouseMoved, self).__init__(x, y, button, modifiers)
