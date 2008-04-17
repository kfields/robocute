from node import *
from block.block import *
'''
Warning:  Do not import this.  These are hidden implementation classes.
Only scene.py and builder.py should need to import this file.
'''

class Cell(AbstractCell):
    def __init__(self):
        super(AbstractCell, self).__init__()

    def remove_node(self, node):
        top = self[len(self) - 1]
        if(isinstance(top, GroupBlock)):
            top.remove_node(node)
            return
        #else
        self.remove(node)

    def push_node(self, node):
        if(len(self) ==0):
            self.append(node)
            return
        #else
        top = self[len(self) - 1]
        #top is group ... add to group
        if(isinstance(top, GroupBlock)):
            top.add_node(node)
        elif(isinstance(top, Block)):
            #top is block ... push on stack        
            self.append(node)
        #top is person, place or thing
        #pop top, push group, push old top and new node
        else:
            oldTop = self.pop()
            top = GroupBlock()
            top.add_node(oldTop)
            top.add_node(node)
            self.append(top)

class Row(list):
    def __init__(self, colCount = WORLD_GRID_COL_MAX):
        super(Row, self).__init__()
        self.colCount = colCount
    
    def validate(self):
        #prevent underage
        data = self
        if len(data) < self.colCount:
            i = 0
            while i < self.colCount:
                data.append(Cell())
                i += 1
        
class GridVu(Vu):
    def __init__(self, node):
        super(GridVu, self).__init__(node)
    
    def draw(self, graphics):
        g = graphics.copy()
        query = g.query 
        #
        invScaleX = 1. / g.scaleX
        invScaleY = 1. / g.scaleY
        invScaleZ = 1. / g.scaleZ
        #
        coordX = self.node.coordX
        coordY = self.node.coordY 
        #
        width = int((g.width + BLOCK_WIDTH) * invScaleX)
        height = int((g.height + BLOCK_ROW_HEIGHT) * invScaleY)
        bottom = int((g.y - BLOCK_ROW_HEIGHT) * invScaleY)
        top = bottom + height
        left = int((g.x - BLOCK_WIDTH) * invScaleX)
        right = left + width
        #
        rowCount = self.node.rowCount
        rowMax = rowCount - 1 
        colCount = self.node.colCount
        colMax = colCount - 1         
        #
        r1 = int(top * INV_BLOCK_ROW_HEIGHT) - coordY
        if(r1 < 0):
            r1 = 0
        if(r1 > rowMax):
            r1 = rowMax
        #  
        r2 = int(bottom * INV_BLOCK_ROW_HEIGHT) - coordY
        if(r2 < 0):
            r2 = 0
        if(r2 > rowMax):
            r2 = rowMax
        #
        c1 = int(left * INV_BLOCK_WIDTH) - coordX
        if(c1 < 0):
            c1 = 0
        if(c1 > colMax):
            c1 = colMax          
        #  
        c2 = int(right * INV_BLOCK_WIDTH) - coordX
        if(c2 < 0):
            c2 = 0
        if(c2 > colMax):
            c2 = colMax
        #
        r = r1
        data = self.node.data
        while(r >= r2): #rows in sheet
            if len(data[r]) == 0:
                r += 1
                continue
            #else
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
                if(query):
                   query.cellX = c
                   query.cellY = r
                for node in cell:
                    vu = node.vu
                    if(vu != None):                        
                        g.translate(blitX, blitY + blitUp)
                        vu.draw(g) 
                        blitUp = blitUp + vu.get_stack_height()
                c += 1
            r -= 1            

#WORLD_GRID_ROW_MAX = 64
#WORLD_GRID_COL_MAX = 64

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
                
    def create_row(self):
        row = Row(self.colCount)
        return row
    
    def create_cell(self):
        cell = Cell()
        return cell
    
    def validate(self):
        #prevent underage
        data = self.data
        if len(data) < self.rowCount:
            i = 0
            while i < self.rowCount:
                row = Row()
                row.validate()
                data.append(row)
                i += 1

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
    
    def get_top_at(self, coord):
        cell = self.get_cell_at(coord)
        if(not cell):
            return None
        length = len(cell)
        if(length == 0):
            raise Exception()
        top = cell[length-1]
        return top

    def get_top_block_at(self, coord):
        cell = self.get_cell_at(coord)
        if(not cell):
            return None
        length = len(cell)
        if(length == 0):
            raise Exception()
        for top in reversed(cell):
            if(isinstance(top, GroupBlock)): #cripes!  It is shallow testing! Good in a way.
                break            
            if(isinstance(top, Block)):
                break
        return top

    '''
    This will get the transform of a group member
    '''
    def get_node_transform(self, targetNode, coord):
        if(isinstance(targetNode, Block)):
           return get_block_transform(targetNode, coord)
        #else        
        cell = self.get_cell_at(coord)
        blitUp = 0                                    
        for node in cell:
            vu = node.vu
            blitUp = blitUp + vu.get_stack_height()
            if(isinstance(node, GroupBlock)):
                return vu.get_member_transform(Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT + blitUp), targetNode)
        blitY = (coord.y * BLOCK_ROW_HEIGHT)
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t
    '''
    This will get the transform of any block.
    '''    
    def get_block_transform(self, block, coord):
        cell = self.get_cell_at(coord)
        blitUp = 0
        for node in cell:
            if(node == block):
                break
            vu = node.vu
            if(vu != None):
                blitUp = blitUp + vu.get_stack_height()        
        blitY = (coord.y * BLOCK_ROW_HEIGHT)
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t
