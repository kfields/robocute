
from node import *

class Brain(object):
    def __init__(self, node):
        super(Brain, self).__init__()
        self.node = node
        self.scene = None #get's set during registration of node.
        self.coord = Coord(0,0) #brain knows where node is at roughly
        self.old_coord = self.coord
        #
        self.on_move = None #need callback for camera!!!
    
    def get_node(self):
        return self.node
    
    def set_scene(self, scene):
        self.scene = scene

    def get_scene(self):
        return self.scene
    
    def set_coord(self, coord):
        self.old_coord = self.coord
        self.coord = coord
        
    def get_coord(self):
        return self.coord
    
    def do(self, msg):
        pass