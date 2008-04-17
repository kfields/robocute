
from node import *

class Brain(object):
    def __init__(self, node):
        super(Brain, self).__init__()
        self.node = node
        self.app = None #get's set during registration of node.
        self.grid = None
        self.scene = None        
        #
        self.__coord = Coord(0,0) #brain knows where node is at roughly
        self.old_coord = self.coord
        #
        self.on_move = None #need callback for camera!!!

    def register(self, app, coord):
        self.app = app
        self.grid = app.world.get_grid_at(coord)
        self.scene = app.scene
        self.coord = coord
            
    def set_coord(self, coord):
        self.old_coord = self.coord
        self.__coord = coord
        
    def get_coord(self):
        return self.__coord
    
    coord = property(get_coord, set_coord)
    
    def do(self, msg):
        pass