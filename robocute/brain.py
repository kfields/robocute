
from robocute.base import *
from robocute import globe

class Brain(Base):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.app = globe.app
        self.scene = None
        self.user = None

    def register(self, app, coord = None):
        super().register(app, coord)
        self.scene = app.scene
        
    def bind(self, user):
        self.user = user
    
    def unbind(self):
        self.user = None
        
    def start(self):
        pass

    def do(self, msg):
        pass
