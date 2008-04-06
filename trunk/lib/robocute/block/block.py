import data

from robocute.node import *
from robocute.vu import *

BLOCK_WIDTH = 101
BLOCK_HEIGHT = 171
BLOCK_STACK_HEIGHT = 40
BLOCK_ROW_HEIGHT = 85

class BlockVu(ImageVu):
    def __init__(self, node, imgSrc):
        super(BlockVu, self).__init__(node, imgSrc)
    #fixme:Hmmm...could we move this into the base?  Eliminate this class?
    def get_stack_height(self):
        return self.node.height * BLOCK_STACK_HEIGHT
    
class Block(AbstractNode):
    def __init__(self):
        super(Block, self).__init__()
        self.height = 1
    def get_height(self):
        return self.height

class GroupBlockVu(Vu):
    def __init__(self, node):
        super(GroupBlockVu, self).__init__(node)

    def get_stack_height(self):
        if(len(self.node.nodes) != 0):
            vu = self.node.nodes[0].get_vu()
            if(vu != None):
                return vu.get_stack_height() #fixme:temporary hack.  calc tallest node!
        #else
        return 0
        
    def draw(self, graphics):
        g = graphics.copy()
        for node in self.node.nodes:
            vu = node.get_vu()
            if(vu != None):
                vu.draw(g)
                g.x += 10
                g.y -= 10
                
class GroupBlock(Node):
    def __init__(self):
        super(GroupBlock, self).__init__()
        self.nodes = []
        self.vu = GroupBlockVu(self)

    def get_nodes(self):
        return self.nodes
        
    def add_node(self, node):
        self.nodes.append(node)
        
    def remove_node(self, node):
        self.nodes.remove(node)
    
    def has_vacancy(self):
        return True

class SpawnBlock(GroupBlock):
    def __init__(self, spawn):
        super(SpawnBlock, self).__init__()
        self.spawn = spawn
        self.add_node(spawn)

    def remove_node(self, node):
        super(SpawnBlock, self).remove_node(node)
        if(node == self.spawn):
            spawn = self.spawn.copy()
            del self.spawn
            clock.schedule_once(lambda dt, *args, **kwargs : self.respawn(), 3.)
            
    def respawn(self):
        self.add_node(self.spawn)

class DirtBlock(Block):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = DirtBlock()
        return cls.singleton
        
    def __init__(self):
        super(DirtBlock, self).__init__()
        self.vu = BlockVu(self, 'Dirt Block.png')

    def has_vacancy(self):
        return True
        

class StoneBlock(Block):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = StoneBlock()
        return cls.singleton
    
    def __init__(self):
        super(StoneBlock, self).__init__()
        self.vu = BlockVu(self, 'Stone Block.png')

    def has_vacancy(self):
        return True

class StoneBlockTall(Block):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = StoneBlockTall()
        return cls.singleton
    
    def __init__(self):
        super(StoneBlockTall, self).__init__()
        self.vu = BlockVu(self, 'Stone Block Tall.png')
        self.height = 2

    def has_vacancy(self):
        return True

class RampWest(Block):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = RampWest()
        return cls.singleton
    
    def __init__(self):
        super(RampWest, self).__init__()
        self.vu = BlockVu(self, 'Ramp West.png')

    def has_vacancy(self):
        return True

class RampEast(Block):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = RampEast()
        return cls.singleton
    
    def __init__(self):
        super(RampEast, self).__init__()
        self.vu = BlockVu(self, 'Ramp East.png')

    def has_vacancy(self):
        return True
    
class GrassBlock(Block):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = GrassBlock()
        return cls.singleton
    
    def __init__(self):
        super(GrassBlock, self).__init__()
        self.vu = BlockVu(self, 'Grass Block.png')
    
class WaterBlock(Block):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = WaterBlock()
        return cls.singleton
    
    def __init__(self):
        super(WaterBlock, self).__init__()
        self.vu = BlockVu(self, 'Water Block.png')
