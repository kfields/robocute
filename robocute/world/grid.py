from robocute.node import *
from robocute.block import *
from robocute.pane import *

from .cell import *
from .row import *

class GridLayer(BatchLayer):
    def __init__(self, grid):
        super().__init__('grid')
        self.grid = grid
        
class GridVu(Pane):
    def __init__(self, node):
        super().__init__(node)
        self.layer = GridLayer(node)
        self.tileLayer = self.layer.create_layer()
        self.app = None #needed to register callbacks .. actually didn't work that well!
        #
        self.batching = True
        #self.batching = False
        
    def register(self, app, coord):
        super().register(app, coord)
        self.app = app
        
    def validate(self):
        super().validate()
        if not self.batching:
            return
        #
        self.layer.validate()
        #
        g = Graphics()
        g.clip = None
        self.batch(g)

    def draw(self, graphics):
        if self.invalid:
            self.node.validate() #seems to work the best here ...
        
        if self.batching:
            self.layer.draw(graphics)
            if graphics.query:
                self.query(graphics)
            return
        #else        
        def draw(vu, graphics):
            vu.draw(graphics)
        self.walk(graphics, draw)

    def batch(self, graphics):
        self.layer.reset()
        def batch(vu, graphics):
            graphics.layer = self.tileLayer
            vu.batch(graphics)
        self.walk(graphics, batch)
        
    def query(self, graphics):
        def query(vu, graphics):
            vu.query(graphics)
        self.walk(graphics, query)
        
    '''
    Might be better off with generators for row and column?
    '''
    def walk(self, graphics, callback):
        rows = self.node.rows
        g = graphics.copy()
        query = g.query
        #
        r1, r2, c1, c2 = self.clip(g.clip)
        # print(r1, r2, c1, c2)

        # r = r1
        r = len(rows) - 1
        #
        # print(len(rows))
        while(r >= r2): #rows in sheet
            print(r)
            '''
            if len(rows[r]) == 0:
                r += 1
                continue
            '''
            #else
            g.cellY = self.node.coordY + r
            row = rows[r]
            print(row)
            c = c1
            blitY = r * BLOCK_ROW_HEIGHT
            while(c <= c2): #cells in row
                blitX = c * BLOCK_WIDTH                
                blitUp = 0
                cell = row[c]
                if not cell:
                    c += 1
                    continue
                g.cellX = self.node.coordX + c
                o = 0
                for node in cell:
                    vu = node.vu
                    if(vu != None):
                        g.cellZ = o                        
                        g.translate(blitX, blitY + blitUp)
                        callback(vu, g)
                        blitUp = blitUp +  node.height * BLOCK_STACK_HEIGHT
                    #o += 1
                    o += node.height #hmmm...
                c += 1
            r -= 1            

    def clip(self, clip):
        #
        rowCount = self.node.rowCount
        rowMax = rowCount - 1 
        colCount = self.node.colCount
        colMax = colCount - 1         
        #
        if not clip:
            return rowMax, 0, 0, colMax
        #else  
        posX = self.node.coordX * BLOCK_WIDTH
        posY = self.node.coordY * BLOCK_ROW_HEIGHT
        #
        '''
        topPadding = BLOCK_ROW_HEIGHT
        bottomPadding = BLOCK_ROW_HEIGHT
        leftPadding = BLOCK_WIDTH
        rightPadding = BLOCK_WIDTH
        '''
        topPadding = 0
        bottomPadding = 0
        leftPadding = 0
        rightPadding = 0        
        #
        bottom = clip.bottom - posY
        top = clip.top - posY
        left = clip.left - posX
        right = clip.right - posX
        #
        r1 = int(top * INV_BLOCK_ROW_HEIGHT)
        if(r1 < 0):
            r1 = 0
        if(r1 > rowMax):
            r1 = rowMax
        #  
        r2 = int(bottom * INV_BLOCK_ROW_HEIGHT)
        if(r2 < 0):
            r2 = 0
        if(r2 > rowMax):
            r2 = rowMax
        #
        c1 = int(left * INV_BLOCK_WIDTH)
        if(c1 < 0):
            c1 = 0
        if(c1 > colMax):
            c1 = colMax          
        #  
        c2 = int(right * INV_BLOCK_WIDTH)
        if(c2 < 0):
            c2 = 0
        if(c2 > colMax):
            c2 = colMax
        #

        return r1, r2, c1, c2
    
class Grid(Node):
    def __init__(self, colCount = WORLD_GRID_COL_MAX, rowCount = WORLD_GRID_ROW_MAX):
        super().__init__()
        #
        self.colCount = colCount
        self.rowCount = rowCount
        self.rows = []
        #
        self.vu = GridVu(self)
               
    def validate(self):
        super().validate()
        #prevent underage
        rows = self.rows
        if len(rows) < self.rowCount:
            i = 0
            while i < self.rowCount:
                row = self.create_row()
                row.validate()
                rows.append(row)
                i += 1
        for row in self.rows:
            if row.invalid != 0:
                row.validate()

    def create_row(self):
        row = Row(self.colCount)
        return row

    def build(self, app, world, x, y):
        self.world = world        
        self.gridX = x
        self.gridY = y
        self.coordX = x * self.colCount
        self.coordY = y * self.rowCount
        #do this last!!!
        world.add_grid(self)        
        #prevent underage     
        self.validate()                
        #
        rowNdx = 0
        for row in self.rows:
            row.build(app, self, rowNdx)
            rowNdx += 1
        
    def clone(self):
        clone = Grid(self.colCount, self.rowCount)
        for row in self.rows:
            cloneRow = row.clone()
            clone.rows.append(cloneRow)
        return clone
    
    def valid_coord(self, coord):
        '''
        if coord.x < 0 or coord.x > self.coordX + self.colCount - 1:
            return False
        if coord.y < 0 or coord.y > self.coordY + self.rowCount - 1:
            return False
        '''
        if coord.x < 0 or coord.y < 0:
            return False
        
        return True

    def local_coord(self, coord):
        if coord.x < self.coordX or coord.x > self.coordX + self.colCount - 1:
            return False
        if coord.y < self.coordY or coord.y > self.coordY + self.rowCount - 1:
            return False
        return True
    
    def to_local_coord(self, coord):        
        return Coord(coord.x % self.colCount, coord.y % self.rowCount)
    
    def get_cell_at(self, coord):
        '''
        if(not self.valid_coord(coord)):
            raise Exception('Invalid Coordinates: x: ', coord.x, ' y: ', coord.y)
        '''
        if not self.local_coord(coord):
            return self.world.get_cell_at(coord)
        #else
        return self.rows[coord.y % self.rowCount][coord.x % self.colCount]
    
    '''
    Cell Access Helpers
    '''
    def get_top_at(self, coord):
        cell = self.get_cell_at(coord)
        top = cell.get_top()
        return top

    def get_top_block_at(self, coord):
        cell = self.get_cell_at(coord)
        top = cell.get_top_block()
        return top

    def get_top_transform_at(self, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_top_transform(coord)
        return t
    
    def get_bottom_transform_at(self, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_bottom_transform(coord)
        return t    
    '''
    This will get the transform of a group member
    '''
    def get_node_transform_at(self, targetNode, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_node_transform(targetNode, coord)
        return t
    '''
    This will get the transform of any block.
    '''    
    def get_block_transform_at(self, block, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_block_transform(block, coord)
        return t
