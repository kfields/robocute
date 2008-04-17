
#from ods.catalog import * #dependency problem
#
from widget.widget import *
from widget.list import List
from widget.skin import *
from widget.bubble import *
from pyglet.gl import *
from block.block import *

class Item(Image):
    def __init__(self, name, imgSrc, body, useFn):
        super(Item, self).__init__(imgSrc, useFn)
        self.name = name
        self.body = body
        self.vu = ImageVu(self, imgSrc)
        #
        self.assignments = [] #list of property value tuples
    
    def add_assignment(self, prop, val):
        self.assignments.append( (prop, val) )
        
    def has_assignments(self):
        return not len(self.assignments) == 0

class PageVu(WidgetVu):
    def __init__(self, node, slicesName):
        super(PageVu, self).__init__(node)   
        self.skin = VerticalSkin(slicesName)     
        #fixme:all so temporary ... put into Vu class?  Scaling per Vu. Hmmm... uses_scaling()
        self.scaleX = .25
        self.scaleY = .25
        
    def validate(self):
        super(PageVu, self).validate()
        scaleY = self.scaleY
        #
        for item in self.node.items:
            vu = item.vu
            vu.validate()
            #self.height += int( ( vu.height + self.vspace) *.75 * scaleY)
            self.height += int( ( vu.height + self.vspace) * scaleY)
     
    def draw(self, graphics):
        super(PageVu, self).draw(graphics)
        self.draw_items(graphics)
        
    def draw_items(self, graphics):
        
        scaleX = self.scaleX
        scaleY = self.scaleY
        invScaleX = 1 / scaleX
        invScaleY = 1 / scaleY
        
        g = graphics.copy()
        g.height = self.height
        g.width = self.width
        g.x += self.margin_left
        g.y += ( self.height - self.margin_top)
        #
        g.x = int( g.x * invScaleX)
        gX = g.x
        g.y = int( g.y * invScaleY)

        glPushMatrix()
        glTranslatef(self.margin_left, -self.margin_bottom, 0)
        glScalef(scaleX, scaleY, 1.)
        
        for item in self.node.items:
            vu = item.vu            
            #center horizontally
            g.x = (gX + (g.width * .5) - (vu.width * .5)) * invScaleX
            #
            vu.draw(g)
            #
            g.y -= (vu.height + self.vspace)# *.75                        
        #
        glPopMatrix()
        
class Page(List):
    def __init__(self, name, items = None):
        super(Page, self).__init__(items)
        self.name = name
        self.vu = PageVu(self, 'CatalogBubble')
        self.vu.validate()

class Catalog(Bubble):
    def __init__(self, items):        
        super(Catalog, self).__init__(items)
        self.vu = BubbleVu(self, 'DashBubble')
        self.vu.validate() #necessary evil. :)
        #
        self.pages = {}
        self.nextPages = {}
        self.prevPages = {}
        #
        #rdr = Reader(self, filename, useFn)
        #rdr.read()

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

'''
class Catalog:
    def __init__(self, filename, useFn):
        self.pages = {}
        rdr = Reader(self, filename, useFn)
        rdr.read()
    
    def add_page(self, pageName, page):
        self.pages[pageName] = page
        
    def get_page(self, pageName):
        return self.pages[pageName]
'''