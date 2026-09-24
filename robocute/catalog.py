from crunge import yoga

from crunge.engine.ui.flex import Column


from robocute.builder import Dna
from robocute.widget import *
from robocute.widget.bubble import *


class Page(Column):
    def __init__(self, name, children=None):
        logger.debug(f"Page items: {children}")
        style = yoga.StyleBuilder().width(64).margin(yoga.Edge.ALL, 5).build()
        super().__init__(children=children, style=style)
        self.name = name


BLOCK_FACE = 40  # one block step, in source pixels
FRAME_HEIGHT = 171  # CuteGod frame height
FRAME_WIDTH = 101


class Catalog:
    def __init__(self):
        super().__init__()
        #
        self.pages = {}
        self.nextPages = {}
        self.prevPages = {}
        #
        self.on_item = None

    def create_item(self, dnaType, name, title, img_src, body, assignments):
        def onItem(item):
            self.on_item(item)

        dna = Dna(dnaType, name, title, img_src, body, assignments)

        crop = None
        if dna.type == "tool":
            style = yoga.StyleBuilder().size(32, 32).build()
        else:
            # The art sits lower in the frame the shorter the block is, so
            # trim from the top and keep everything below it.
            top = max(0, FRAME_HEIGHT - BLOCK_FACE * (dna.block_height + 1) - 1)
            crop = (0, top, FRAME_WIDTH, FRAME_HEIGHT - top)
            style = yoga.StyleBuilder().size(64, 64).build()

        item = ItemImage(dna, onItem, style=style, crop=crop)

        return item

    def add_page(self, pageName, page):
        self.pages[pageName] = page

    def get_page(self, pageName):
        return self.pages[pageName]

    def set_next_page(self, pageName, nextPageName):
        self.nextPages[pageName] = nextPageName

    def get_next_page(self, pageName):
        return self.pages[self.nextPages[pageName]]

    def set_prev_page(self, pageName, prevPageName):
        self.prevPages[pageName] = prevPageName

    def get_prev_page(self, pageName):
        return self.pages[self.prevPages[pageName]]
