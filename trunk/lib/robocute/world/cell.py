
from robocute.base import *
from robocute.block import *
from robocute.builder import execute_ctors

class Cell(list):
    def __init__(self):
        super(Cell, self).__init__()
        self.invalid = 0
        self.height = 0
        #
        #self.dna = None
        self.ctors = None
    '''
    def __getstate__(self):
        return self.__dict__
                
    def __setstate__(self, state):
        self.__dict__ = state
    ''' 
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
                
    def build(self, app, row, coord):
        self.row = row        
        #app.build(self.dna, coord, self)
        #build(app, self.dna, coord, self)
        if self.ctors:
            execute_ctors(app, self.ctors, coord, self)
        
    def clone(self):
        clone = Cell()
        #clone.dna = self.dna
        clone.ctors = self.ctors
        return clone

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
                if group.empty():
                    self.remove_node(group) #watchme:recursive
                elif group.redundant():
                    member = group.nodes[0]
                    self.remove_node(group) #watchme:recursive
                    self.push_node(member)
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

