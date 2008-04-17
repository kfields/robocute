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
    def register(self, app, coord):
        super(Bot, self).register(app, coord)
        def start():
            brain = self.brain
            if(brain):
                brain.start()            
        app.add_callback(start)
    '''
    def start(self):
        pass
    '''