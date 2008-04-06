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

DirtBlock_singleton = None

class DirtBlock(Block):
    def __new__(cls, *args, **kargs):
        global DirtBlock_singleton
        if not DirtBlock_singleton:
            obj = object.__new__(cls)
            DirtBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return DirtBlock_singleton
        
    def __init__(self):
        super(DirtBlock, self).__init__()
        self.vu = BlockVu(self, 'Dirt Block.png')

    def has_vacancy(self):
        return True
        
StoneBlock_singleton = None

class StoneBlock(Block):
    def __new__(cls, *args, **kargs):
        global StoneBlock_singleton
        if not StoneBlock_singleton:
            obj = object.__new__(cls)
            StoneBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return StoneBlock_singleton
    
    def __init__(self):
        super(StoneBlock, self).__init__()
        self.vu = BlockVu(self, 'Stone Block.png')

    def has_vacancy(self):
        return True

StoneBlockTall_singleton = None

class StoneBlockTall(Block):
    def __new__(cls, *args, **kargs):
        global StoneBlockTall_singleton
        if not StoneBlockTall_singleton:
            obj = object.__new__(cls)
            StoneBlockTall_singleton = obj
            obj.__init__(*args, **kargs)
        return StoneBlockTall_singleton
    
    def __init__(self):
        super(StoneBlockTall, self).__init__()
        self.vu = BlockVu(self, 'Stone Block Tall.png')
        self.height = 2

    def has_vacancy(self):
        return True

RampWest_singleton = None

class RampWest(Block):
    def __new__(cls, *args, **kargs):
        global RampWest_singleton
        if not RampWest_singleton:
            obj = object.__new__(cls)
            RampWest_singleton = obj
            obj.__init__(*args, **kargs)
        return RampWest_singleton
    
    def __init__(self):
        super(RampWest, self).__init__()
        self.vu = BlockVu(self, 'Ramp West.png')

    def has_vacancy(self):
        return True

RampEast_singleton = None

class RampEast(Block):
    def __new__(cls, *args, **kargs):
        global RampEast_singleton
        if not RampEast_singleton:
            obj = object.__new__(cls)
            RampEast_singleton = obj
            obj.__init__(*args, **kargs)
        return RampEast_singleton
    
    def __init__(self):
        super(RampEast, self).__init__()
        self.vu = BlockVu(self, 'Ramp East.png')

    def has_vacancy(self):
        return True

GrassBlock_singleton = None
    
class GrassBlock(Block):
    def __new__(cls, *args, **kargs):
        global GrassBlock_singleton
        if not GrassBlock_singleton:
            obj = object.__new__(cls)
            GrassBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return GrassBlock_singleton
    
    def __init__(self):
        super(GrassBlock, self).__init__()
        self.vu = BlockVu(self, 'Grass Block.png')

'''
This is an interesting solution.  Too bad I don't want to use it. :(
http://mail.python.org/pipermail/python-list/2008-February/476992.html
...
class RDFObject(object):
    _cache = {}   # class variable is shared among all RDFObject
instances
    class __metaclass__(type):
        def __call__(cls, *args, **kwargs):
            return cls.__new__(cls, *args, **kwargs)
    def __new__(cls, uri, *args, **kargs):
        if uri not in cls._cache:
            obj = object.__new__(cls)
            cls._cache[uri] = obj
            obj.__init__(uri, *args, **kargs)
        return cls._cache[uri]
    def __init__(self, uri):
        self.uri = uri
        print self.__class__, uri
'''
WaterBlock_singleton = None

class WaterBlock(Block):
    def __new__(cls, *args, **kargs):
        global WaterBlock_singleton
        if not WaterBlock_singleton:
            obj = object.__new__(cls)
            WaterBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return WaterBlock_singleton
    def __init__(self):
        super(WaterBlock, self).__init__()
        self.vu = BlockVu(self, 'Water Block.png')
