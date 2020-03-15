from builder import Dna

#from ods.catalog import * #dependency problem
#
from widget import *
#from widget.list import List
from skin import *
from widget.bubble import *
from pyglet.gl import *

class ItemVu(ImageVu):
    def __init__(self, node, imgSrc):
        self.width = 0
        self.height = 0
        super(ItemVu, self).__init__(node, imgSrc)
        self.scaleX = .25
        self.scaleY = .25                
        self.width = int( self.image.width * self.scaleX ) 
        self.height = int ( self.image.height * self.scaleY)
    
    def draw(self, graphics):
        g = graphics.copy()
        glPushMatrix()
        glTranslatef(graphics.x, graphics.y, graphics.z)        
        glScalef(self.scaleX, self.scaleY, 1.)
        g.x = 0
        g.y = 0
        super(ItemVu, self).draw(g)
        glPopMatrix()

class ToolVu(ImageVu):
    def __init__(self, node, imgSrc):
        super(ToolVu, self).__init__(node, imgSrc)
        
class Item(Image):
    def __init__(self, dna, useFn):
        super(Item, self).__init__(dna.imgSrc, useFn)
        self.dna = dna
        if dna.type == 'tool':
            self.vu = ToolVu(self, dna.imgSrc)
        else:
            self.vu = ItemVu(self, dna.imgSrc)

class PageVu(WidgetVu):
    def __init__(self, node, slicesName):
        super(PageVu, self).__init__(node)   
        self.skin = VerticalSkin(FileSkinData(slicesName, 3))
        
    def validate(self):
        self.content.width = self.skin.content.width
        self.content.height = 0
        for item in self.node.items:
            vu = item.vu
            vu.validate()
            self.content.height += vu.height + self.vspace
        #
        super(PageVu, self).validate()
     
    def draw(self, graphics):
        super(PageVu, self).draw(graphics) #call to get skin drawn.
        self.draw_items(graphics)
        
    def draw_items(self, graphics):        
        g = graphics.copy()
        #g.y += self.margin_bottom
        g.y += self.content.height - self.margin_top - self.vspace
        #
        #g.x += self.margin_left
        gX = g.x
        
        for item in self.node.items:
            vu = item.vu            
            #center horizontally
            g.x = gX + (self.content.width * .5) - (vu.width * .5)
            #
            vu.draw(g)
            #
            g.y -= (vu.height + self.vspace)                        
        
class Page(Widget):
    def __init__(self, name, items = None):
        super(Page, self).__init__(items)
        self.name = name
        self.vu = PageVu(self, 'CatalogBubble')
        self.vu.validate()

class Catalog(object):
    def __init__(self):        
        super(Catalog, self).__init__()
        #
        self.pages = {}
        self.nextPages = {}
        self.prevPages = {}
        #
        self.on_item = None

    def create_item(self, dnaType, name, title, imgSrc, body, assignments):
        def onItem(item):
            self.on_item(item)
        dna = Dna(dnaType, name, title, imgSrc, body, assignments)
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
