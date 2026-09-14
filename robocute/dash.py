from crunge.engine.overlay import Overlay

from robocute.layer import *
from robocute.vu import *
from robocute.node import *

class DrawerVu(Vu):
    def __init__(self, node):
        super().__init__(node)   

    def draw(self, graphics):
        g = graphics.copy()
        for node in self.node.nodes:
            vu = node.vu
            if(vu != None):
                vu.draw(g)
                #g.y += vu.height + 10
                g.y += vu.height
    
class Drawer(Node):
    def __init__(self, node = None):
        super().__init__()
        self.nodes = []        
        if node:
            self.nodes.append(node)

    def _seat(self):
        super()._seat()
        self.add(DrawerVu(self))
        
    def add_node(self, node):
        self.nodes.append(node)
        
    def remove_node(self, node):
        self.nodes.remove(node)

class Dash(Overlay):
    def __init__(self, name):
        super().__init__(name)
    
    def create_drawer(self, drawerName, node = None):
        drawer = Drawer(node)
        return drawer

    '''
    def draw(self, graphics):
        g = graphics.copy()
        for node in self.nodes:
            vu = node.vu
            vu.draw(g)
            g.x += vu.width + 10
    '''