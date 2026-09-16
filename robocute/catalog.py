from crunge import yoga

from robocute.builder import Dna
from robocute.widget import *
from robocute.skin import *
from robocute.widget.bubble import *


class ItemVu(ImageVu):
    def __init__(self, img_src):
        self.width = 0
        self.height = 0
        super().__init__(img_src)
        self.scaleX = 0.25
        self.scaleY = 0.25
        # self.width = int( self.image.width * self.scaleX )
        # self.height = int ( self.image.height * self.scaleY)


class ToolVu(ImageVu):
    def __init__(self, img_src):
        super().__init__(img_src)


class Item(Image):
    def __init__(self, dna: Dna, useFn):
        super().__init__(dna.img_src, useFn)
        self.dna = dna
        """
        if dna.type == 'tool':
            self.add(ToolVu(dna.img_src))
        else:
            self.add(ItemVu(dna.img_src))
        """


class Page(GameWidget):
    def __init__(self, name, items=None):
        logger.debug(f"Page items: {items}")
        # style=yoga.StyleBuilder().size_percent(100, 100).margin(yoga.Edge.ALL, 5).build()
        style = yoga.Style()
        # style.set_flex_grow(0.75)
        # style.set_flex_grow(1)
        super().__init__(items, style=style)
        self.name = name
        # self.add(PageVu(self, 'CatalogBubble'))

    def on_layout(self):
        super().on_layout()
        logger.debug(f"Page layout updated: {self.size}")


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
        item = Item(dna, onItem)
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
