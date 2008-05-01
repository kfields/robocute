
from robocute.widget.bubble import *

class Catalog(Bubble):
    def __init__(self, items, catalog):
        super(Catalog, self).__init__(items)
        self.catalog = catalog
        self.vu = BubbleVu(self, 'DashBubble')
        self.vu.validate() #necessary evil. :)

    def get_page(self, pageName):
        return self.catalog.get_page(pageName)

    def get_next_page(self, pageName):
        return self.catalog.get_next_page(pageName)

    def get_prev_page(self, pageName):
        return self.catalog.get_prev_page(pageName)
