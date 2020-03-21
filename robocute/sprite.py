
import pyglet
from pyglet.gl import *

from vu import *
from texture import *

from tile import *

class SpriteVu(TileVu):  #just hang around with the tiles for now ...
    def __init__(self, node, imgSrc):
        super().__init__(node, imgSrc)
        self.strip = TileStrip()
        self.texture = self.strip.register(self.imgSrc, self.image)