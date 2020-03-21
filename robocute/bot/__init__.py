from robocute.entity import *
from robocute.sprite import *

#was going to name it bot ... robo goes with the theme
    
class BotVu(SpriteVu):
    def __init__(self, node, imgSrc):
        super().__init__(node, imgSrc)
        self.hotHeight = 120 #fixme:use constant

class Bot(Entity):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vacancy = False
        self.height = 2
        self.vu = BotVu(self, 'robocute.png')        
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