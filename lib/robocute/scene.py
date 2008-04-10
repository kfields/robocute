import os, sys
import zipfile
import xml.dom.minidom

import data
from grid import *
from layer import *
from builder import *
from mouse import Mouse
from user.user import *

from pyglet.gl import *

OD_TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'

def get_text(node):
    text = ''
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            text = text+get_text(child)
        elif child.nodeType == child.TEXT_NODE:
            text = text+child.nodeValue

    return text

class Reader(object):

    def __init__(self, scene, filename):
        self.scene = scene
        self.grid = scene.grid
        self.builder = scene.get_builder()
        self.filename = filename
        #self.m_odf = zipfile.ZipFile(filename)
        self.m_odf = data.load_zip(filename)
        self.filelist = self.m_odf.infolist()
        #
        ostr = self.m_odf.read('content.xml')
        self.content = xml.dom.minidom.parseString(ostr)
        #
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
    def read(self):
        tileRow = []
        self.read_sheets()
        
    def read_sheets(self):
        doc = self.content
        sheets = doc.getElementsByTagNameNS(OD_TABLE_NS, 'table')
        for sheet in sheets:
            self.read_sheet(sheet)
            
    def read_sheet(self, sheet):
        sheet_name = sheet.getAttributeNS(OD_TABLE_NS, 'name')
        self.read_rows(sheet)
        
    def read_rows(self, sheet):
        rows = sheet.getElementsByTagNameNS(OD_TABLE_NS, 'table-row')
        self.scene.row_count = len(rows)
        rowNdx = 0
        for row in rows:
            self.read_row(row, rowNdx)
            rowNdx += 1
        #
        firstRow = self.grid[0]
        colCount = len(firstRow)
        self.scene.col_count = colCount
        #
        self.grid.reverse() #need to reverse to match OpenGL coordinate system.

    def read_row(self, row, rowNdx):
        #new
        repCountStr = row.getAttributeNS(OD_TABLE_NS, 'number-rows-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        while(repCount > 0):
            gridRow = self.read_cells(row, rowNdx)
            self.grid.append(gridRow)
            repCount = repCount - 1
                    
    def read_cells(self, row, rowNdx):
        gridRow = Row()
        cells = row.getElementsByTagNameNS(OD_TABLE_NS, 'table-cell')
        colNdx = 0        
        for cell in cells:
            #self.read_cell(cell, gridRow, Coord(colNdx, rowNdx))
            self.read_cell(cell, gridRow, Coord(colNdx, (self.scene.row_count-1) - rowNdx))
            colNdx += 1            
        return gridRow
        
    def read_cell(self, cell, gridRow, coord):
        repCountStr = cell.getAttributeNS(OD_TABLE_NS, 'number-columns-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        cellTxt = get_text(cell)
        cell = Cell()
        #self.builder.produce(cellTxt, (colNdx, (self.scene.row_count-1) - rowNdx), cell)
        self.builder.produce(cellTxt, coord, cell)
                
        while(repCount > 0):
            gridRow.append(cell)
            repCount = repCount - 1
'''
'''

class Scene(object):
    
    def __init__(self, win, filename):
        super(Scene, self).__init__()
        #
        self.window = win
        #
        self.bots = []        
        #
        self.builder = Builder(self)
        #
        self.bgImg = image.load(data.filepath('image/clouds.jpg'))
        #
        self.grid = Grid() # List of lists of lists.  3 dimensions.
        self.row_count = 0
        self.col_count = 0
        #
        rdr = Reader(self, filename)
        rdr.read()
        #
        self.bubbles = BubbleLayer(self)
        #
        self.dash = Dash(self)
        self.mice = MouseLayer(self)
        #User creation has to come last!!!
        self.user = User(self)        
    
    def start(self):
        for bot in self.bots:
            brain = bot.brain
            if(brain):
                brain.start()
        
    def get_window(self):
        return self.window
    
    def get_builder(self):
        return self.builder
    
    def get_user(self):
        return self.user
        
    def valid_coord(self, coord):
        if(coord.x < 0 or coord.x > self.col_count - 1):
            return False
        if(coord.y < 0 or coord.y > self.row_count - 1):
            return False
        return True

    def get_cell_at(self, coord):
        if(not self.valid_coord(coord)):
            raise Exception('Invalid Coordinates: x: ', coord.x, ' y: ', coord.y)
        #else
        return self.grid[coord.y][coord.x]
    
    def get_top_at(self, coord):
        cell = self.get_cell_at(coord)
        if(not cell):
            return None
        length = len(cell)
        if(length == 0):
            raise Exception()
        top = cell[length-1]
        return top

    def get_top_block_at(self, coord):
        cell = self.get_cell_at(coord)
        if(not cell):
            return None
        length = len(cell)
        if(length == 0):
            raise Exception()
        for top in reversed(cell):
            if(isinstance(top, GroupBlock)): #cripes!  It is shallow testing! Good in a way.
                break            
            if(isinstance(top, Block)):
                break
        return top

    def can_transfer(self, node, srcCoord, dstCoord):
        #boundary check
        if(not self.valid_coord(dstCoord)):
            return False
        #destination check
        top = self.get_top_block_at(dstCoord)
        if(not top.has_vacancy()):
           return False
       #good to go
        return True
        
    def transfer(self, node, srcCoord, dstCoord):
       if(not self.can_transfer(node, srcCoord, dstCoord)):
           return False
       #else
       srcCell = self.get_cell_at(srcCoord)
       srcCell.remove_node(node)
       #
       dstCell = self.get_cell_at(dstCoord)
       dstCell.push_node(node)
       #
       brain = node.get_brain()
       if(brain != None):
           brain.set_coord(dstCoord)
    '''
    Bots
        fixme:this class is getting too fat!!!
    '''
    def add_bot(self, bot):
        self.bots.append(bot)
    def remove_bot(self, bot):
        self.bots.remove(bot)
    '''
    Avatar Support
    fixme:this may need to go into User
    '''
    def create_avatar(self, name):
        node = Avatar()
        if(not node):
            raise Exception('No Avatar found in scene!!!')
        brain = node.get_brain()
        if(brain == None):
           raise Exception("This node has no brain!")
        #
        return brain
    '''
    Rendering
    '''
    def draw(self, graphics):
        self.draw_background(graphics)
        #
        glPushMatrix()
        #
        glTranslatef(-graphics.x, -graphics.y, graphics.z)
        #
        self.draw_rows(graphics)
        #
        self.bubbles.draw(graphics)
        #
        glPopMatrix()
        #
        self.dash.draw(graphics)
        #
        self.mice.draw(graphics)

    def draw_background(self, graphics):
        bgWidth = self.bgImg.width
        bgHeight = self.bgImg.height
        
        blitY = 0
        while(blitY < self.window.height):
            blitX = 0
            while(blitX < self.window.width):
                self.bgImg.blit(blitX, blitY, 0)
                blitX = blitX + bgWidth
            blitY = blitY + bgHeight
    
    def draw_rows(self, graphics):
        g = graphics.copy()
        #
        #better to expand the view I think.
        #
        width = g.width + BLOCK_WIDTH
        height = g.height + BLOCK_ROW_HEIGHT
        bottom = g.y - BLOCK_ROW_HEIGHT
        top = bottom + height
        left = g.x - BLOCK_WIDTH
        right = left + width
        #
        r1 = int(top * INV_BLOCK_ROW_HEIGHT)
        if(r1 < 0):
            r1 = 0
        if(r1 > self.row_count-1):
            r1 = self.row_count-1
        #  
        r2 = int(bottom * INV_BLOCK_ROW_HEIGHT)
        if(r2 < 0):
            r2 = 0
        if(r2 > self.row_count-1):
            r2 = self.row_count-1
        #
        c1 = int(left * INV_BLOCK_WIDTH)
        if(c1 < 0):
            c1 = 0
        if(c1 > self.col_count-1):
            c1 = self.col_count-1          
        #  
        c2 = int(right * INV_BLOCK_WIDTH)
        if(c2 < 0):
            c2 = 0
        if(c2 > self.col_count-1):
            c2 = self.col_count-1
        #
        r = r1
        while(r >= r2): #rows in sheet
            c = c1
            blitY = r * BLOCK_ROW_HEIGHT
            row = self.grid[r]
            while(c <= c2): #cells in row
                blitX = c * BLOCK_WIDTH                
                blitUp = 0
                nodes = row[c]                         
                for node in nodes:
                    vu = node.get_vu()
                    if(vu != None):                        
                        g.translate(blitX, blitY + blitUp)
                        vu.draw(g) 
                        blitUp = blitUp + vu.get_stack_height()

                c += 1
            r -= 1            
    '''
    This will get the transform of a group member
    '''
    def get_node_transform(self, targetNode, coord):
        if(isinstance(targetNode, Block)):
           return get_block_transform(targetNode, coord)
        #else        
        cell = self.get_cell_at(coord)
        blitUp = 0                                    
        for node in cell:
            vu = node.get_vu()
            blitUp = blitUp + vu.get_stack_height()
            if(isinstance(node, GroupBlock)):
                return vu.get_member_transform(Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT + blitUp), targetNode)
        blitY = (coord.y * BLOCK_ROW_HEIGHT)
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t
    '''
    This will get the transform of any block.
    '''    
    def get_block_transform(self, block, coord):
        cell = self.get_cell_at(coord)
        blitUp = 0
        for node in cell:
            if(node == block):
                break
            vu = node.get_vu()
            if(vu != None):
                blitUp = blitUp + vu.get_stack_height()        
        blitY = (coord.y * BLOCK_ROW_HEIGHT)
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t

    '''
    Bubbles:
    '''
    def add_bubble(self, bubble):
        self.bubbles.add_node(bubble)
    
    def remove_bubble(self, bubble):
        self.bubbles.remove_node(bubble)

    '''
    Mouse Support
    '''
    def add_mouse(self, mouse):
        self.mice.add_node(mouse)
        
    def remove_mouse(self, mouse):
        self.mice.remove_node(mouse)

