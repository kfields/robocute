import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.resource.resource_manager import ResourceManager

from robocute.entity import *

class BotVu(SpriteVu):
    def __init__(self, imgSrc):
        print(f"Loading sprite from {imgSrc}")
        path = ResourceManager().resolve_path("${resources}/image/" + imgSrc)
        sprite = SpriteLoader().load(path)

        super().__init__(sprite)
        self.hotHeight = 120 #fixme:use constant

class Bot(Entity):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vacancy = False
        #self.height = 2
        #self.size = glm.vec2(1, 1, 1)
        self.add(BotVu('robocute.png'))

    '''
    def _seat(self):
        super()._seat()
        self.add(BotVu('robocute.png'))
    '''
    
    '''
    This is that post constructor we need.
    Idea is to add ourselves to Scene list of spreaders, fillers, mappers, etc.
    '''
    def register(self, app, coord):
        super().register(app, coord)
        def start():
            brain = self.brain
            if(brain):
                brain.start()            
        app.add_callback(start)
    '''
    def start(self):
        pass
    '''