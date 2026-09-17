from crunge.engine.brain import Brain

from robocute.base import *
from robocute import globe

class BaseBrain(Brain):
    def __init__(self):
        super().__init__()
        self.app = globe.app
        self.view = None

    @property
    def grid(self):
        return self.node.grid

    def bind(self, user):
        self.view = user
    
    def unbind(self):
        self.view = None
        
    def start(self):
        pass

    def do(self, msg):
        pass
