
from node import Node
from node import Coord
from vu import ImageVu
from message import Message
from mailbox import Mailbox

class Result(Coord):
    def __init__(self, node, cellX, cellY, cellZ):
        Coord.__init__(self, cellX, cellY, cellZ)
        self.node = node
                
class MouseQuery(object):
    def __init__(self, event):
        self.event = event
        self.x = event.x
        self.y = event.y
        self.results = []
    
    def add_result(self, node, cellX, cellY, cellZ):
        self.results.append(Result(node, cellX, cellY, cellZ))
                            
    def process(self):
        if(not self.results):
            return
        #get last result, highest z
        event = self.event
        result = self.results[-1]
        result.node.process(event)
        print(result.node, event)
        
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

class Mousebox(Mailbox):
    def __init__(self):
        super(Mousebox, self).__init__()
        
    def create_query(self, event):
        return MouseQuery(event) 
    '''
    event handlers
    '''
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        pass
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
    
class MultiMousebox(Mailbox):
    def __init__(self):
        super(MultiMousebox, self).__init__()
                
    def on_mouse_motion(self, x, y, dx, dy):
        for box in self.boxes:
            box.on_mouse_motion(x, y, dx, dy)
    
    def on_mouse_press(self, x, y, button, modifiers):
        for box in self.boxes:
            box.on_mouse_press(x, y, button, modifiers)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for box in self.boxes:
            box.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        