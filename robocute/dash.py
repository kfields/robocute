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
        self.vu = DrawerVu(self)
        self.vu.validate()
        
    def add_node(self, node):
        vu = node.vu
        vu.validate()
        self.vu.width = vu.width #fixme:what a hack! 
        self.nodes.append(node)
        
    def remove_node(self, node):
        self.nodes.remove(node)

class Dash(NodeLayer):
    def __init__(self, parent, name, order):
        super().__init__(parent, name, order)
        #self.drawers = {}
    
    def create_drawer(self, drawerName, node = None):
        drawer = Drawer(node)
        #self.drawers = drawer
        #self.add_node(drawer)
        return drawer
    
    def draw(self, graphics):
        g = graphics.copy()
        for node in self.nodes:
            vu = node.vu
            vu.draw(g)
            g.x += vu.width + 10
