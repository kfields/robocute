import operator #needed for sorting

from loguru import logger

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.sprite.instanced import InstancedSpriteVuGroup
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.resource.resource_manager import ResourceManager

from robocute.entity import *
from robocute.vu import *
from robocute.builder import find_dna, add_class, add_classes

sprite_loader = SpriteLoader()

class BlockVu(SpriteVu):
    def __init__(self, img_src):
        #logger.debug(f"Loading sprite from {img_src}")
        path = ResourceManager().resolve_path("${resources}/image/" + img_src)
        sprite = sprite_loader.load(path)
        #logger.debug(f"Sprite loaded from {sprite}")
        super().__init__(sprite)

    def validate(self):
        super().validate()
        self.hotHeight = self.node.height * BLOCK_HOT_HEIGHT
        
class Block(Entity):
    groupable = False
    def __init__(self, dna):
        super().__init__(dna)

class GroupBlockVu(InstancedSpriteVuGroup):
    def __init__(self):
        super().__init__()

    def validate(self):
        super().validate()

    '''
    def draw(self, graphics):
        def draw(vu, graphics):
            vu.draw(graphics)
        self.walk(graphics, draw)
    '''
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
    def __init__(self, dna = None):
        if not dna:
            dna = find_dna('GroupBlock')
        super().__init__(dna)
        self.nodes = []
        #self.add(GroupBlockVu())
        self.vacancy = True
        self.dirty = True

    def update(self, delta_time: float):
        height = 0
        for node in self.nodes:
            node_block_height = node.block_height
            if node_block_height > height:
                height = node_block_height
        self.block_height = height
        super().update(delta_time)
        
    def push_node(self, node):
        self.nodes.append(node)
        #self.nodes.sort(key=operator.attrgetter('z')) #fixme:hack to sort by width ... just use width!
        self.update(0.)
        
    def remove_node(self, node):
        self.nodes.remove(node)
        self.update(0.)
        
    def empty(self):
        return len(self.nodes) == 0

    def redundant(self):
        return len(self.nodes) == 1

    def get_member_transform(self, transform, memberNode):
        t = transform.copy()
        for node in self.nodes:
            t.x += 10
            t.y -= 10
            if node == memberNode:
                break
        t.y += node.height * BLOCK_STACK_HEIGHT
        return t

    def yield_visuals(self):
        """Yield the group's own visual, then its members', bottom to top."""
        yield from super().yield_visuals()
        for node in self.nodes:
            yield from node.yield_visuals()

class HomeBlock(GroupBlock):
    def __init__(self):
        super().__init__()
    def register(self, app, coord):
        app.add_home(self, coord)

# todo: this is really broke
class SpawnBlock(GroupBlock):
    def __init__(self, spawn):
        super().__init__()
        self.spawn = spawn
        #self.add_node(spawn)

    def schedule_respawn(self, delay):
            def respawn():
                self.respawn()
            clock.schedule_once(lambda dt, *args, **kwargs : respawn(), delay)
        
    def remove_node(self, node):
        super().remove_node(node)
        if node == self.spawn:
            self.spawn = self.spawn.copy()
            self.schedule_respawn(3.)
            
    def respawn(self):
        if len(self.nodes) == 0:
            self.add_node(self.spawn)
        else:
            self.schedule_respawn(3.)           

add_class(SpawnBlock)