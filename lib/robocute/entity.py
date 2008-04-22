
from base import *
import node
import brain 

class Entity(node.Node):
    groupable = True
    
    def __init__(self, fn = None):
        super(Entity, self).__init__()
        self.height = 1
        self.vacancy = False
                            
class Brain(brain.Brain):
    def __init__(self, node):
        super(Brain, self).__init__(node)
        self.grid = None
        #
        self.__coord = Coord(0,0) #brain knows where node is at roughly
        self.old_coord = self.coord
        #
        self.on_move = None #need callback for camera!!!

    def register(self, app, coord):
        super(Brain, self).register(app, coord)
        self.grid = app.world.get_grid_at(coord)
        self.coord = coord
            
    def set_coord(self, coord):
        self.old_coord = self.coord
        self.__coord = coord
        
    def get_coord(self):
        return self.__coord
    
    coord = property(get_coord, set_coord)