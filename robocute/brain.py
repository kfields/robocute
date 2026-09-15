from crunge.engine.ai import Brain

from robocute.base import *
from robocute import globe

class BaseBrain(Brain):
    def __init__(self):
        super().__init__()
        self.app = globe.app
        self.view = None
        self.user = None

    def register(self, app, coord = None):
        super().register(app, coord)
        self.view = app.scene
        
    def bind(self, user):
        self.user = user
    
    def unbind(self):
        self.user = None
        
    def start(self):
        pass

    def do(self, msg):
        pass
