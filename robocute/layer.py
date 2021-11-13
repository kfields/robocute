import pyglet

import robocute.sprite

from robocute.base import *

LAYER_ANY = -1
LAYER_DEFAULT = 0

class Layer(Base):
    def __init__(self, parent, name = None, order = LAYER_ANY):
        super().__init__()
        self.parent = parent
        self.name = name
        self.order = order
        if parent:
            self.root = parent.root
        else:
            self.root = self
            
        self.layers = []
        self.orderIncrement = 1        
        self.orderCount = self.order + self.orderIncrement 
    
    def create_layer(self, name = None, order = LAYER_ANY):
        if order == LAYER_ANY:
            self.orderCount += self.orderIncrement
            order = self.orderCount
        layer = Layer(self, name, order)
        self.layers.append(layer)
        return layer
        
    def draw(self, graphics):
        pass
    
class NodeLayer(Layer):
    def __init__(self, parent, name, order):
        super().__init__(parent, name, order)
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)
    
    def remove_node(self, node):
        self.nodes.remove(node)
        
    def draw(self, graphics):
        g = graphics.copy()
        for node in self.nodes:
            vu = node.vu
            if(vu != None):
                t = node.get_transform()
                g.translate(t.x, t.y)
                vu.draw(g)

class AbstractGroupLayer(Layer):
    def __init__(self, parent = None, name = None, order = LAYER_DEFAULT):
        super().__init__(parent, name, order)
        self.group = None
        
    def create_layer(self, name = None, order = LAYER_ANY):
        if order == LAYER_ANY:
            self.orderCount += self.orderIncrement
            order = self.orderCount
        layer = GroupLayer(self, name, order)
        self.layers.append(layer)
        return layer
        
class GroupLayer(AbstractGroupLayer):
    def __init__(self, parent, name, order):
        super().__init__(parent, name, order)
        self.group = pyglet.graphics.OrderedGroup(order, self.root.group)
        self.groups = {}

    def register_group(self, group):
        if group in self.groups:
            #index = self.groups.index(group)
            #group = self.groups[index]
            group = self.groups[group]
        else:
            #self.groups.append(group)
            self.groups[group] = group
        return group
    
class BatchLayer(AbstractGroupLayer):
    def __init__(self, name):
        super().__init__(None, name)
        self.batch = None
        self.group = pyglet.graphics.Group()
        self.reset()
        
    def reset(self):
        self.batch = pyglet.graphics.Batch()

    def draw(self, graphics):
        self.batch.draw()
        
class RootLayer(Layer):
    def __init__(self, name):
        super().__init__(None, name)
        
