
from app import *
import world
from ods.grid import *

class World(world.World):
    def __init__(self, app, filename, gridRowMax = WORLD_GRID_ROW_MAX, gridColMax = WORLD_GRID_COL_MAX):
        #super(World, self).__init__(app, gridRowMax, gridColMax)
        super(World, self).__init__(app, 12, 12)
        self.filename = filename

    def create_grid(self, x, y):
        grid = Grid(self, x, y, self.gridRowMax, self.gridColMax)
        rdr = Reader(self.filename, self.app, grid)
        rdr.read()
        return grid

class Game(App):
    def __init__(self, filename):
        super(Game, self).__init__(filename)
    
    def create_world(self):
        world = World(self, self.filename)
        return world
    
    def create_user(self):
        #user = User(self)
        user = Player(self)
        #user = Designer(self)
        return user
