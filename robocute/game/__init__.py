
from robocute.base import *

class Game(Base):
    def __init__(self, app, name):
        super().__init__()
        self.app = app
        self.window = app.window
        self.name = name
        #
        self.catalog = self.create_catalog()        
        #
        self.world = self.load_or_create_world()
        self.scene = self.create_scene()
        self.world.vu = self.scene
        
    def save(self):
        self.save_world()
        
    def save_world(self):
        self.world.save()
            
    def load_or_create_world(self):
        world = self.load_world()
        if not world:
            world = self.create_world()
        return world
    
    def load_world(self):
        world = None
        return world
    
    def create_world(self):
        return None
    
    def create_scene(self):
        return None
    
    def create_catalog(self):
        return None
    
