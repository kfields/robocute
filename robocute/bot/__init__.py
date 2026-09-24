from loguru import logger

import glm

from crunge.engine.scheduler import Scheduler
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.resource.resource_manager import ResourceManager

from robocute.entity import *
from .bot_brain import BotBrain

class BotVu(SpriteVu):
    def __init__(self, img_src):
        #logger.debug(f"Loading sprite from {img_src}")
        path = ResourceManager().resolve_path("${resources}/image/" + img_src)
        sprite = SpriteLoader().load(path)

        super().__init__(sprite)
        self.hotHeight = 120 #fixme:use constant

class Bot(Entity):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vacancy = False
        self.block_height = 2

    def construct_vu(self):
        self.vu = self.add_chip(BotVu('robocute.png'))
    
    '''
    This is that post constructor we need.
    Idea is to add ourselves to Scene list of spreaders, fillers, mappers, etc.
    '''

    def _ready(self):
        super()._ready()
        def start(delta_time: float):
            brain = self.brain
            if(brain):
                brain.start()
        #app.add_callback(start)
        Scheduler().schedule_once(start)

    '''
    def register(self, app, coord):
        super().register(app, coord)
        def start(delta_time: float):
            brain = self.brain
            if(brain):
                brain.start()
        #app.add_callback(start)
        Scheduler().schedule_once(start)
    '''

    '''
    def start(self):
        pass
    '''