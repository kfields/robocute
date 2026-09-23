from functools import partial

from crunge import yoga
from crunge import sdl

from crunge.engine.ui import Image as CrungeImage
from crunge.engine.ui.chips import GestureChip


class Image(CrungeImage):
    def __init__(self, img_src, fn=None, style=None, crop=None):
        src = "${resources}/image/" + img_src
        #style = yoga.StyleBuilder().size(64, 64).margin(yoga.Edge.ALL, 5).build()
        #style = yoga.StyleBuilder().size(64, 64).build()
        #super().__init__(src=src, style=style)
        super().__init__(src=src, style=style, crop=crop)
        on_tap = partial(fn, self) if fn else None
        self.add_chip(GestureChip(on_tap))
