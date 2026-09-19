from . import globe

from crunge.engine.scheduler import Scheduler
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.resource.resource_manager import ResourceManager

from robocute.brain import BaseBrain
from robocute.node import GameNode
from robocute.base import Coord

class EntityVu(SpriteVu):
    def __init__(self, img_src):
        #logger.debug(f"Loading sprite from {img_src}")
        path = ResourceManager().resolve_path("${resources}/image/" + img_src)
        sprite = SpriteLoader().load(path)

        super().__init__(sprite)
        self.hotHeight = 120 #fixme:use constant

class Entity(GameNode):
    groupable = True
    
    def __init__(self, dna = None, fn = None):
        super().__init__(dna, fn)
        self.block_height = 1
        self.vacancy = True
        self.grid = None
        self.construct_vu()

    def construct_vu(self):
        if self.dna.img_src:
            self.vu = self.add_chip(EntityVu(self.dna.img_src))

class EntityBrain(BaseBrain):
    def __init__(self):
        super().__init__()
        #self.grid = None
        #
        #self.__coord = Coord(0,0) #brain knows where node is at roughly
        #self.old_coord = self.coord
        #
        self.on_move = None #need callback for camera!!!

    @property
    def coord(self):
        return self.node.coord if self.node is not None else None
    
    def register(self, app, coord):
        self.grid = self.app.world.get_grid_at(coord)
        self.coord = coord
    '''
    def set_coord(self, coord):
        self.old_coord = self.coord
        self.__coord = coord
        
    def get_coord(self):
        return self.__coord
    
    coord = property(get_coord, set_coord)
    '''