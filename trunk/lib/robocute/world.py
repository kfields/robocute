from grid import *

class World(AbstractNode):
    def __init__(self, app, gridRowMax = WORLD_GRID_ROW_MAX, gridColMax = WORLD_GRID_COL_MAX):
        super(World, self).__init__()
        self.app = app
        self.gridRowMax = gridRowMax
        self.gridColMax = gridColMax        
        self.gridcache = {}
        
    def create_grid(self, x, y):
        grid = Grid(self, x, y, self.gridRowMax, self.gridColMax)
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
        
        gridX = coord.x / gridColMax
        #cellX = coord.x % gridColMax
        gridY = coord.y / gridRowMax
        #cellY = coord.y % gridRowMax
                
        return self.get_grid(gridX, gridY)
        
    def get_grid(self, x, y):
        c1 = self.gridcache
        if not y in c1:
            c2 = {}
            grid = self.create_grid(x, y)
            c2[x] = grid
            c1[y] = c2 
        else:
            c2 = c1[y]
            if not x in c2:
                grid = self.create_grid(x, y)
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

    def get_node_transform(self, targetNode, coord):
        grid = self.get_grid_at(coord)
        return grid.get_node_transform(targetNode, coord)

    def get_block_transform(self, block, coord):
        grid = self.get_grid_at(coord)
        return grid.get_block_transform(block, coord)
    