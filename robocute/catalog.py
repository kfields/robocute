from crunge import yoga

#from crunge.engine.widget import Widget
from crunge.engine.ui.flex import Column


from robocute.builder import Dna
from robocute.widget import *
from robocute.widget.bubble import *

from .base import BLOCK_HEIGHT

class ItemVu(ImageVu):
    def __init__(self, img_src):
        self.width = 0
        self.height = 0
        super().__init__(img_src)
        self.scaleX = 0.25
        self.scaleY = 0.25
        # self.width = int( self.image.width * self.scaleX )
        # self.height = int ( self.image.height * self.scaleY)


'''
class Item(Image):
    def __init__(self, dna: Dna, useFn):
        crop = None
        if dna.type == 'tool':
            style = yoga.StyleBuilder().size(32, 32).build()
        else:
            #crop = (0, 0, 64, 64)
            crop=(0, 40, 100, 131)
            style = yoga.StyleBuilder().size(64, 64).build()

        super().__init__(dna.img_src, useFn, style=style, crop=crop)
        self.dna = dna
        
        logger.debug(f"Created item: {dna}")
'''

class Item(Image):
    def __init__(self, dna: Dna, useFn, style=None, crop=None):
        super().__init__(dna.img_src, useFn, style=style, crop=crop)
        self.dna = dna
        
        logger.debug(f"Created item: {dna}")

class Page(Column):
    def __init__(self, name, children=None):
        logger.debug(f"Page items: {children}")
        # style=yoga.StyleBuilder().size_percent(100, 100).margin(yoga.Edge.ALL, 5).build()
        #style = yoga.Style()
        # style.set_flex_grow(0.75)
        # style.set_flex_grow(1)
        style=yoga.StyleBuilder().width(64).margin(yoga.Edge.ALL, 5).build()
        super().__init__(children=children, style=style)
        self.name = name
        # self.add_chip(PageVu(self, 'CatalogBubble'))

BLOCK_FACE = 40        # one block step, in source pixels
FRAME_HEIGHT = 171     # CuteGod frame height
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
        if dna.type == 'tool':
            style = yoga.StyleBuilder().size(32, 32).build()
        else:
            # The art sits lower in the frame the shorter the block is, so
            # trim from the top and keep everything below it.
            top = max(0, FRAME_HEIGHT - BLOCK_FACE * (dna.block_height + 1) - 1)
            crop = (0, top, FRAME_WIDTH, FRAME_HEIGHT - top)
            style = yoga.StyleBuilder().size(64, 64).build()

        item = Item(dna, onItem, style=style, crop=crop)

        return item
    '''
    def create_item(self, dnaType, name, title, img_src, body, assignments):
        def onItem(item):
            self.on_item(item)

        dna = Dna(dnaType, name, title, img_src, body, assignments)


        crop = None
        if dna.type == 'tool':
            style = yoga.StyleBuilder().size(32, 32).build()
        else:
            #crop = (0, 0, 64, 64)
            #crop=(0, 40, 100, 131)
            crop = (0, dna.block_height * BLOCK_HEIGHT, 100, 131)
            style = yoga.StyleBuilder().size(64, 64).build()
    
        item = Item(dna, onItem, style=style, crop=crop)

        return item
    '''

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
