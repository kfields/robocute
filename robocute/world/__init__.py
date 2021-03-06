
import os
import pickle
from .grid import *
import robocute.persist.grid.native

class World(AbstractNode):
    def __init__(self, app, name, gridRowMax = WORLD_GRID_ROW_MAX, gridColMax = WORLD_GRID_COL_MAX):
        super().__init__()
        self.app = app
        self.name = name        
        self.gridRowMax = gridRowMax
        self.gridColMax = gridColMax        
        self.gridcache = {}
        
    def save(self):
        self.save_grids()
        
    def save_grids(self):
        for cacheRow in self.gridcache.values():
            for grid in cacheRow.values():
                self.save_grid(grid)
    
    def get_filepath(self):
        path = 'storage/game/' + self.name + '/' 
        return path
    
    def get_grid_filepath(self, x, y):
        path = self.get_filepath()
        path += 'grid/'
        path += self.name + '_' + str(x) + '_' + str(y) + '.grid'
        return str(path)
        
    def save_grid(self, grid):
        x = grid.gridX
        y = grid.gridY
        path = self.get_grid_filepath(x, y)
        path_dir = os.path.dirname(path)
        os.makedirs(path_dir, exist_ok=True)
        writer = robocute.persist.grid.native.Writer(path, grid)
        writer.write()
        
    def load_or_generate_grid(self, x, y):
        grid = self.load_grid(x, y)
        if not grid:
            grid = self.generate_grid(x, y)
        #
        grid.build(self.app, self, x, y)
        #
        grid.register(self.app)        
            
        return grid

    def load_grid(self, x, y):
        grid = None
        path = self.get_grid_filepath(x, y)
        print(path)
        if os.path.exists(path):
            grid = self.create_grid(x, y)
            rdr = robocute.persist.grid.native.Reader(path, grid)
            rdr.read()
               
        return grid
    
    def generate_grid(self, x, y):
        return self.create_grid(self, x, y)
    
    def create_grid(self, x, y):
        grid = Grid(self.gridRowMax, self.gridColMax)
        return grid
        
    def add_grid(self, grid):
        x = grid.gridX
        y = grid.gridY
        c1 = self.gridcache
        if not y in c1:
            c2 = {}
            c1[y] = c2
            c2[x] = grid
        else:
            c2 = c1[y]
            if not x in c2:
                c2[x] = grid

    def get_grid_at(self, coord):
        gridRowMax = self.gridRowMax
        gridColMax = self.gridColMax
        gridX = int(coord.x / gridColMax)
        gridY = int(coord.y / gridRowMax)
        return self.get_grid(gridX, gridY)
        
    def get_grid(self, x, y):
        c1 = self.gridcache
        if not y in c1:
            c2 = {}
            grid = self.load_or_generate_grid(x, y)
            c2[x] = grid
            c1[y] = c2 
        else:
            c2 = c1[y]
            if not x in c2:
                grid = self.load_or_generate_grid(x, y)
                c2[x] = grid
            else:
                grid = c2[x]
        return grid
    
    def exists_grid(self, x, y):
        c1 = self.gridcache
        if not y in c1:
            return False
        else:
            c2 = c1[y]
        if not x in c2:
            return False
        #else
        return True
    '''
    Grid Access
    '''        
    def valid_coord(self, coord):
        grid = self.get_grid_at(coord)
        return grid.valid_coord(coord)
    
    def get_cell_at(self, coord):
        grid = self.get_grid_at(coord)
        return grid.get_cell_at(coord)
    
    def get_top_at(self, coord):
        grid = self.get_grid_at(coord)
        return grid.get_top_at(coord)

    def get_top_block_at(self, coord):
        grid = self.get_grid_at(coord)
        return grid.get_top_block_at(coord)

    def get_top_transform_at(self, coord):
        grid = self.get_grid_at(coord)
        return grid.get_top_transform_at(coord)
    
    def get_bottom_transform_at(self, coord):
        grid = self.get_grid_at(coord)
        return grid.get_bottom_transform_at(coord)

    def get_node_transform_at(self, targetNode, coord):
        grid = self.get_grid_at(coord)
        return grid.get_node_transform_at(targetNode, coord)