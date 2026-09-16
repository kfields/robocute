from crunge.engine.ai import Brain

from robocute.base import *
from robocute import globe

class BaseBrain(Brain):
    def __init__(self):
        super().__init__()
        self.app = globe.app
        self.view = globe.view
        self.user = None

    @property
    def grid(self):
        return self.node.grid

    def bind(self, user):
        self.user = user
    
    def unbind(self):
        self.user = None
        
    def start(self):
        pass

    def do(self, msg):
        pass
