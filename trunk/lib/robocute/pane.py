
import pyglet

from vu import Vu

from layer import *

class Pane(Vu):    
    def __init__(self, node):
        super(Pane, self).__init__(node)
        self.layer = None