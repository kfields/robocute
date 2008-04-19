import data
import operator #needed for sorting

from pyglet import clock

from robocute.node import *
from robocute.vu import *
#
BLOCK_WIDTH = 101
BLOCK_HEIGHT = 171
BLOCK_STACK_HEIGHT = 40
BLOCK_ROW_HEIGHT = 85
#
#decimals behind 1 important!!! else you get zero!!!???
INV_BLOCK_WIDTH = 1. / BLOCK_WIDTH
INV_BLOCK_HEIGHT = 1. / BLOCK_HEIGHT
INV_BLOCK_STACK_HEIGHT = 1. / BLOCK_STACK_HEIGHT
INV_BLOCK_ROW_HEIGHT = 1. / BLOCK_ROW_HEIGHT
#
WORLD_GRID_ROW_MAX = 64
WORLD_GRID_COL_MAX = 64
WORLD_GRID_CACHE_ROW_COUNT= 64
WORLD_GRID_CACHE_COL_COUNT = 64
#
WORLD_GRID_WIDTH = WORLD_GRID_COL_MAX * BLOCK_WIDTH
WORLD_GRID_HEIGHT = WORLD_GRID_ROW_MAX * BLOCK_ROW_HEIGHT
WORLD_GRID_CACHE_WIDTH = WORLD_GRID_CACHE_COL_COUNT * WORLD_GRID_WIDTH
WORLD_GRID_CACHE_HEIGHT = WORLD_GRID_CACHE_ROW_COUNT * WORLD_GRID_HEIGHT
#
INV_WORLD_GRID_WIDTH = 1. / WORLD_GRID_WIDTH
INV_WORLD_GRID_HEIGHT = 1. / WORLD_GRID_HEIGHT
INV_WORLD_GRID_CACHE_WIDTH = 1. / WORLD_GRID_CACHE_WIDTH
INV_WORLD_GRID_CACHE_HEIGHT = 1. / WORLD_GRID_CACHE_HEIGHT
'''
'''
#class BlockVu(ImageVu):
class BlockVu(MeshImageVu):
    def __init__(self, node, imgSrc):
        super(BlockVu, self).__init__(node, imgSrc)
        self.stack_height = self.node.height * BLOCK_STACK_HEIGHT
        #self.add_hotspot(HotSpot(0,0,self.width,BLOCK_ROW_HEIGHT))
    #fixme:Hmmm...could we move this into the base?  Eliminate this class?
    '''
    def get_stack_height(self):
        return self.node.height * BLOCK_STACK_HEIGHT
    '''
    
class Block(AbstractNode):
    def __init__(self):
        super(Block, self).__init__()
        self.height = 1
    def get_height(self):
        return self.height

class GroupBlockVu(Vu):
    def __init__(self, node):
        super(GroupBlockVu, self).__init__(node)
        self.stack_height = 0
    #def get_stack_height(self):
        '''
        if(len(self.node.nodes) != 0):
            vu = self.node.nodes[0].vu
            if(vu != None):
                return vu.get_stack_height() #fixme:temporary hack.  calc tallest node!
        #else
        '''
       # return 0
        
    def draw(self, graphics):
        g = graphics.copy()
        for node in self.node.nodes:
            vu = node.vu
            if(vu != None):
                vu.draw(g)
                g.x += 10
                g.y -= 10
    
    def get_member_transform(self, transform, memberNode):
        t = transform.copy()
        for node in self.node.nodes:
            vu = node.vu
            if(vu != None):
                t.x += 10
                t.y -= 10
            if(node == memberNode):
                break
        #t.y += vu.get_stack_height()
        t.y += vu.stack_height
        return t
        
class GroupBlock(Node):
    def __init__(self):
        super(GroupBlock, self).__init__()
        self.nodes = []
        self.vu = GroupBlockVu(self)

    def get_nodes(self):
        return self.nodes
        
    def add_node(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=operator.attrgetter('z'))
        
    def remove_node(self, node):
        self.nodes.remove(node)
    
    def has_vacancy(self):
        return True

class HomeBlock(GroupBlock):
    def __init__(self):
        super(HomeBlock, self).__init__()
    def register(self, app, coord):
        app.add_home(self, coord)

class SpawnBlock(GroupBlock):
    def __init__(self, spawn):
        super(SpawnBlock, self).__init__()
        self.spawn = spawn
        self.add_node(spawn)

    def schedule_respawn(self, delay):
            def respawn():
                self.respawn()
            clock.schedule_once(lambda dt, *args, **kwargs : respawn(), delay)
        
    def remove_node(self, node):
        super(SpawnBlock, self).remove_node(node)
        if(node == self.spawn):
            self.spawn = self.spawn.copy()
            self.schedule_respawn(3.)
            
    def respawn(self):
        if(len(self.nodes) == 0):
            self.add_node(self.spawn)
        else:
            self.schedule_respawn(3.)           

