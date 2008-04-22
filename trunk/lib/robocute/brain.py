
from base import *

class Brain(Base):
    def __init__(self, node):
        super(Brain, self).__init__()
        self.node = node
        self.app = None #get's set during registration of node.
        self.scene = None
        self.user = None

    def register(self, app, coord):
        super(Brain, self).register(app, coord)
        self.app = app
        self.scene = app.scene
        
    def bind(self, user):
        self.user = user
    
    def unbind(self):
        self.user = None
        
    def start(self):
        pass

    def do(self, msg):
        pass
