import data
import operator #needed for sorting

from robocute.entity import *
from robocute.tile import *

from robocute.builder import find_dna

class BlockVu(TileVu):
    def __init__(self, node, imgSrc):
        super(BlockVu, self).__init__(node, imgSrc)

    def validate(self):
        super(BlockVu, self).validate()
        self.hotHeight = self.node.height * BLOCK_HOT_HEIGHT
        
class Block(Entity):
    groupable = False
    def __init__(self, dna):
        super(Block, self).__init__(dna)

class GroupBlockVu(Vu):
    def __init__(self, node):
        super(GroupBlockVu, self).__init__(node)

    def validate(self):
        super(GroupBlockVu, self).validate()

    def draw(self, graphics):
        def draw(vu, graphics):
            vu.draw(graphics)
        self.walk(graphics, draw)

    def batch(self, graphics):
        def batch(vu, graphics):
            vu.batch(graphics)
        self.walk(graphics, batch)

    def query(self, graphics):
        def query(vu, graphics):
            vu.query(graphics)
        self.walk(graphics, query)
    
    def walk(self, graphics, callback):
        g = graphics.copy()
        for node in self.node.nodes:
            vu = node.vu
            if vu != None:
                callback(vu, g)
                g.x += 10
                g.y -= 10
    
    def get_member_transform(self, transform, memberNode):
        t = transform.copy()
        for node in self.node.nodes:
            vu = node.vu
            if vu != None:
                t.x += 10
                t.y -= 10
            if node == memberNode:
                break
        t.y += node.height * BLOCK_STACK_HEIGHT
        return t
        
class GroupBlock(Block):
    '''
    def __new__(cls, *args, **kargs):
        obj = object.__new__(cls)
        dna = cls.dna
        obj.__init__(dna, *args, **kargs)
        return obj
    '''
    def __init__(self, dna = None):
        if not dna:
            dna = find_dna('GroupBlock')
        super(GroupBlock, self).__init__(dna)
        self.nodes = []
        self.vu = GroupBlockVu(self)
        self.vacancy = True

    def update(self):
        height = 0
        for node in self.nodes:
            nodeHeight = node.height
            if nodeHeight > height:
                height = nodeHeight
        self.height = height
        
    def push_node(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=operator.attrgetter('z')) #fixme:hack to sort by width ... just use width!
        self.update()
        
    def remove_node(self, node):
        self.nodes.remove(node)
        self.update()
        
    def empty(self):
        return len(self.nodes) == 0

    def redundant(self):
        return len(self.nodes) == 1

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
        if node == self.spawn:
            self.spawn = self.spawn.copy()
            self.schedule_respawn(3.)
            
    def respawn(self):
        if len(self.nodes) == 0:
            self.add_node(self.spawn)
        else:
            self.schedule_respawn(3.)           

