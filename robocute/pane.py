
import pyglet

from robocute.vu import Vu

from robocute.layer import *

class Pane(Vu):    
    def __init__(self, node):
        super().__init__(node)
        self.layer = None