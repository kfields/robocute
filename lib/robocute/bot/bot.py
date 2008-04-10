from robocute.node import *
from robocute.vu import *
from brain import Brain

#was going to name it bot ... robo goes with the theme
    
class BotVu(ImageVu):
    def __init__(self, node, imgSrc):
        super(BotVu, self).__init__(node, imgSrc)
    def get_stack_height(self):
        return 100 #necessary for SpeechBubble!

class Bot(Node):
    def __init__(self):
        super(Bot, self).__init__()
        self.brain = None
        self.vu = BotVu(self, 'robocute.png')        
    '''
    This is that post constructor we need.
    Idea is to add ourselves to Scene list of spreaders, fillers, mappers, etc.
    '''
    def register(self, scene, coord):
        super(Bot, self).register(scene, coord)
        scene.add_bot(self)
        
    def start(self):
        pass