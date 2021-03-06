
from robocute.base import *
from robocute.node import Node
import robocute.brain

class Entity(Node):
    groupable = True
    
    def __init__(self, dna = None, fn = None):
        super().__init__(dna, fn)
        self.height = 1
        #self.vacancy = False
        self.vacancy = True
                            
class Brain(robocute.brain.Brain):
    def __init__(self, node):
        super().__init__(node)
        self.grid = None
        #
        self.__coord = Coord(0,0) #brain knows where node is at roughly
        self.old_coord = self.coord
        #
        self.on_move = None #need callback for camera!!!

    def register(self, app, coord):
        super().register(app, coord)
        self.grid = app.world.get_grid_at(coord)
        self.coord = coord
            
    def set_coord(self, coord):
        self.old_coord = self.coord
        self.__coord = coord
        
    def get_coord(self):
        return self.__coord
    
    coord = property(get_coord, set_coord)