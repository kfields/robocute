from node import *
from block.block import *
from pane import *
'''
Warning:  Do not import this.  These are hidden implementation classes.
Only scene.py and builder.py should need to import this file.
'''

class Cell(list):
    def __init__(self, row):
        super(Cell, self).__init__()
        self.row = row
        self.invalid = 0
        self.height = 0
        
    def invalidate(self, flag = 1):
        if self.invalid == 0:
            self.row.invalidate()
        self.invalid |= flag
    
    def validate(self):
        self.invalid = 0
        
    def update(self):
        height = 0
        for node in self:
            height += node.height
        self.height = height
                
    #can't assume group is top any more. :(
    def find_group(self):
        for node in self:
            if isinstance(node, GroupBlock):
                return node
        return None                
                
    def push_node(self, node):
        self.invalidate()
        if len(self) ==0:
            self.append(node)
            self.update()
            return
        #else
        top = self[-1]
        if node.groupable:
            group = self.find_group()        
            if group:
                group.push_node(node)
            elif top.groupable:
                oldTop = self.pop()
                top = GroupBlock()
                top.push_node(oldTop)
                top.push_node(node)
                self.append(top)
            else:
                self.append(node)
        else:
            self.append(node)
        self.update() 

    def pop_node(self):
        node = self[-1]
        self.remove(node)
        self.update()        
        return node
        
    def remove_node(self, node):
        self.invalidate()
        if node.groupable:
            group = self.find_group()
            if group:
                group.remove_node(node)
                self.update()
                return
        #else
        self.remove(node)
        self.update()
    
    def get_top(self):
        length = len(self)
        if(length == 0):
            return None
        top = self[-1]
        return top

    def get_top_block(self):
        length = len(self)
        if(length == 0):
            return None
        for top in reversed(self):
            if(isinstance(top, GroupBlock)): #cripes!  It is shallow testing! Good in a way.
                break            
            if(isinstance(top, Block)):
                break
        return top

    '''
    Get transform at top of cell
    '''    
    def get_top_transform(self, coord):
        t = Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT)
        t.y += self.height * BLOCK_STACK_HEIGHT
        return t

    '''
    Get transform at bottom of cell
    '''    
    def get_bottom_transform(self, coord):
        t = Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT)
        return t

    '''
    Get transform of node at coordinate
    '''    
    def get_node_transform(self, targetNode, coord):
        if(isinstance(targetNode, Block)):
           return get_block_transform(targetNode, coord)
        #else
        blitUp = 0                                    
        for node in self:
            vu = node.vu
            blitUp = blitUp + node.height * BLOCK_STACK_HEIGHT
            if(isinstance(node, GroupBlock)):
                return vu.get_member_transform(Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT + blitUp), targetNode)
        blitY = (coord.y * BLOCK_ROW_HEIGHT)
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t

    '''
    This will get the transform of any block.
    '''    
    def get_block_transform(self, block, coord):
        blitUp = 0
        for node in self:
            if(node == block):
                break
            vu = node.vu
            if(vu != None):
                blitUp = blitUp + node.height * BLOCK_STACK_HEIGHT
        blitY = (coord.y * BLOCK_ROW_HEIGHT)
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t

class Row(list):
    def __init__(self, grid, colCount = WORLD_GRID_COL_MAX):
        super(Row, self).__init__()
        self.grid = grid
        self.colCount = colCount
        self.invalid = 0
        
    def invalidate(self, flag = 1):
        if self.invalid == 0:
            self.grid.invalidate()
        self.invalid |= flag
       
    def validate(self):
        self.invalid = 0
        #prevent underage
        data = self
        if len(data) < self.colCount:
            i = 0
            while i < self.colCount:
                data.append(self.create_cell())
                i += 1
        for cell in self:
            if cell.invalid != 0:            
                cell.validate()

    def create_cell(self):
        cell = Cell(self)
        return cell

class GridLayer(BatchLayer):
    def __init__(self, grid):
        super(GridLayer, self).__init__('grid')
        self.grid = grid
        
class GridVu(Pane):
    def __init__(self, node):
        super(GridVu, self).__init__(node)
        self.layer = GridLayer(node)
        self.tileLayer = self.layer.create_layer()
        self.app = None #needed to register callbacks .. actually didn't work that well!
        #
        self.batching = True
        #self.batching = False
        
    def register(self, app, coord):
        super(GridVu, self).register(app, coord)
        self.app = app
        
    def validate(self):
        super(GridVu, self).validate()
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
        g = graphics.copy()
        query = g.query
        #
        r1, r2, c1, c2 = self.clip(g.clip)
        r = r1
        #
        data = self.node.data
        while(r >= r2): #rows in sheet
            if len(data[r]) == 0:
                r += 1
                continue
            #else
            g.cellY = self.node.coordY + r
            row = data[r]            
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
    def __init__(self, world, x, y, colCount = WORLD_GRID_COL_MAX, rowCount = WORLD_GRID_ROW_MAX):
        super(Grid, self).__init__()
        self.world = world
        self.gridX = x
        self.gridY = y
        self.coordX = x * colCount
        self.coordY = y * rowCount
        #
        self.colCount = colCount
        self.rowCount = rowCount
        self.data = []
        #
        self.vu = GridVu(self)
        #do this last!!!
        world.add_grid(self)
        
       
    def validate(self):
        super(Grid, self).validate()
        #prevent underage
        data = self.data
        if len(data) < self.rowCount:
            i = 0
            while i < self.rowCount:
                row = self.create_row()
                row.validate()
                data.append(row)
                i += 1
        for row in self.data:
            if row.invalid != 0:
                row.validate()

    def create_row(self):
        row = Row(self, self.colCount)
        return row

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
        #return self.data[coord.y][coord.x]
        return self.data[coord.y % self.rowCount][coord.x % self.colCount]
    
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
