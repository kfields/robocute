from builder import builder_dict
from builder import build_item

#from ods.catalog import * #dependency problem
#
from widget import *
#from widget.list import List
from widget.skin import *
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
    def __init__(self, type, name, title, imgSrc, body, assignments, useFn):
        super(Item, self).__init__(imgSrc, useFn)
        self.type = type
        self.name = name
        self.title = title
        self.body = body
        if type == 'tool':
            self.vu = ToolVu(self, imgSrc)
        else:
            self.vu = ItemVu(self, imgSrc)
        #
        self.assignments = assignments #list of property value tuples
    
    def __call__(self, *args, **kargs):
        #print self.body
        return build_item(self)
        
    def add_assignment(self, prop, val):
        self.assignments.append( (prop, val) )
        
    def has_assignments(self):
        return not len(self.assignments) == 0

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

    def create_item(self, itemType, name, title, imgSrc, body, assignments):
        def onItem(item):
            self.on_item(item)        
        item = Item(itemType, name, title, imgSrc, body, assignments, onItem)
        #globals()[name] = item
        #klass = type(str(name), (object,), {})
        #globals()[name] = klass
        #builder_dict[name] = klass
        builder_dict[name] = item
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
