
from robocute.base import *

class Game(Base):
    def __init__(self, app, name):
        super(Game, self).__init__()
        self.app = app
        self.window = app.window
        self.name = name
        #
        self.catalog = self.create_catalog()        
        #
        self.world = self.create_world()
        self.scene = self.create_scene()
        self.world.vu = self.scene
    
    def create_world(self):
        return None
    
    def create_scene(self):
        return None
    
    def create_catalog(self):
        return None