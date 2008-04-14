import os, sys
import zipfile
import xml.dom.minidom

import data
from widget.widget import *
from widget.list import List
from widget.skin import *
from widget.bubble import *
from pyglet.gl import *
from block.block import *

OD_TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'

def get_text(node):
    text = ''
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            text = text+get_text(child)
        elif child.nodeType == child.TEXT_NODE:
            text = text+child.nodeValue

    return text

DNDX_PROP = 0
DNDX_VAL = 1
DNDX_IMG = 3
DNDX_SEQ = 5
DNDX_EXTRA = DNDX_SEQ + 1
 
class Reader(object):
    
    def __init__(self, catalog, filename, useFn):
        self.useFn = useFn
        self.catalog = catalog
        self.page = None
        #self.scene = scene
        #self.grid = scene.grid
        #self.builder = scene.get_builder()
        self.filename = filename
        #self.m_odf = zipfile.ZipFile(filename)
        self.m_odf = data.load_zip(filename)
        self.filelist = self.m_odf.infolist()
        #
        ostr = self.m_odf.read('content.xml')
        self.content = xml.dom.minidom.parseString(ostr)
            
    def read(self):
        tileRow = []
        self.read_sheets()
        
    def read_sheets(self):
        doc = self.content
        sheets = doc.getElementsByTagNameNS(OD_TABLE_NS, 'table')
        for sheet in sheets:
            self.read_sheet(sheet)
            
    def read_sheet(self, sheet):
        self.sheet_name = sheet.getAttributeNS(OD_TABLE_NS, 'name')
        items = []
        self.read_rows(sheet, items)
        #self.page = Page(self.sheet_name, 'CatalogBubble', items)
        page = self.create_page(self.sheet_name, items)
        #self.catalog.add_page(self.sheet_name, self.page)
        self.catalog.add_page(self.sheet_name, page)
        
    def read_rows(self, sheet, items):
        rows = sheet.getElementsByTagNameNS(OD_TABLE_NS, 'table-row')
        #self.scene.row_count = len(rows)
        rowNdx = 0
        for row in rows:
            self.read_row(row, rowNdx, items)
            rowNdx += 1

    def read_row(self, row, rowNdx, items):
        #skip first
        if(rowNdx == 0):
            return
        #else
        repCountStr = row.getAttributeNS(OD_TABLE_NS, 'number-rows-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        while(repCount > 0):
            self.read_cells(row, rowNdx, items)
            repCount = repCount - 1
                    
    def read_cells(self, row, rowNdx, items):
        data = []
        cells = row.getElementsByTagNameNS(OD_TABLE_NS, 'table-cell')
        colNdx = 0        
        for cell in cells:
            self.read_cell(cell, data)
            colNdx += 1
        '''
        DNDX_PROP = 0
        DNDX_VAL = 1
        DNDX_IMG = 3
        DNDX_SEQ = 5
                '''
        datum = data[DNDX_PROP]
        if datum == 'item':
            items.append(self.create_item(data))
            return
        #else
        if datum == 'next':
            self.catalog.set_next_page(self.sheet_name, data[DNDX_VAL])
            return
        #else
        if datum == 'prev':
            self.catalog.set_prev_page(self.sheet_name, data[DNDX_VAL])
            return
        
        
    def read_cell(self, cell, items):
        repCountStr = cell.getAttributeNS(OD_TABLE_NS, 'number-columns-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        cellTxt = get_text(cell)
                
        while(repCount > 0):
            items.append(cellTxt)
            repCount = repCount - 1

    def create_page(self, name, items):
        page = Page(name, items)
        return page
        
    def create_item(self, data):
        #items.append(Item(data[DNDX_VAL], data[DNDX_IMG], data[DNDX_SEQ], self.useFn))
        item = Item(data[DNDX_VAL], data[DNDX_IMG], data[DNDX_SEQ], self.useFn)
        ndx = DNDX_EXTRA
        while ndx < len(data):
            prop = data[ndx]
            if prop == '':
                break
            val = data[ndx+1]
            item.add_assignment(prop, val)
            ndx += 2
        return item
            
            
        
        
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
    def __init__(self, filename, useFn, items):        
        super(Catalog, self).__init__(items)
        self.vu = BubbleVu(self, 'DashBubble')
        self.vu.validate() #necessary evil. :)
        #
        self.pages = {}
        self.nextPages = {}
        self.prevPages = {}
        #
        rdr = Reader(self, filename, useFn)
        rdr.read()

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