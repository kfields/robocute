import os, sys
import zipfile
import xml.dom.minidom

import data
from layer import *
from builder import *
from user import User
from mouse import Mouse

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

class Reader():

    def __init__(self, scene, filename):
        self.scene = scene
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
        rowNdx = 0
        for row in rows:
            self.read_row(row, rowNdx)
            rowNdx += 1
        self.scene.row_count = len(self.scene.rows)
        #self.scene.col_count = len(self.scene.rows[0])
        firstRow = self.scene.rows[0]
        colCount = len(firstRow)
        self.scene.col_count = colCount
            
    def read_row(self, row, rowNdx):
        #new
        repCountStr = row.getAttributeNS(OD_TABLE_NS, 'number-rows-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        while(repCount > 0):
            tileRow = self.read_cells(row, rowNdx)
            self.scene.rows.append(tileRow)
            repCount = repCount - 1
                    
    def read_cells(self, row, rowNdx):
        tileRow = []
        cells = row.getElementsByTagNameNS(OD_TABLE_NS, 'table-cell')
        colNdx = 0        
        for cell in cells:
            self.read_cell(cell, tileRow, [rowNdx, colNdx])
            colNdx += 1            
        return tileRow
        
    def read_cell(self, cell, tileRow, coord):
        repCountStr = cell.getAttributeNS(OD_TABLE_NS, 'number-columns-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        cellTxt = get_text(cell)
        #node = builder.builder.produce(cellTxt)
        nodes = []
        self.builder.produce(cellTxt, coord, nodes)
                
        while(repCount > 0):
            tileRow.append(nodes)
            repCount = repCount - 1
'''
'''

class Scene(object):
    
    def __init__(self, win, filename):
        super(Scene, self).__init__()
        self.window = win
        #
        self.builder = Builder(self)
        #
        self.bgImg = image.load(data.filepath('image/clouds.jpg'))
        #
        self.rows = [] # List of lists of lists.  3 dimensions.
        self.row_count = 0
        self.col_count = 0
        rdr = Reader(self, filename)
        rdr.read()
        #
        #self.bubbles = []
        self.bubbles = BubbleLayer(self)
        #
        self.dash = Dash(self)
        #self.mice = []
        self.mice = MouseLayer(self)
        #This has to come last!!!
        self.user = User(self)        
        
    def get_window(self):
        return self.window
    
    def get_builder(self):
        return self.builder
    
    def get_user(self):
        return self.user
    
    def get_rows(self):
        return self.rows

    def get_row_at(self, y):
        return self.rows[y]
    
    def get_nodes_at(self, coord):
        if(coord[0] < 0 or coord[0] > self.col_count - 1):
            return None
        if(coord[1] < 0 or coord[1] > self.row_count - 1):
            return None        
        row = self.get_row_at(coord[1])
        nodes = row[coord[0]]
        return nodes

    def get_top_at(self, coord):
        nodes = self.get_nodes_at(coord)
        length = len(nodes)
        if(length == 0):
            raise Exception()
        top = nodes[length-1]
        return top

    def get_top_block_at(self, coord):
        nodes = self.get_nodes_at(coord)
        if(not nodes):
            return None
        length = len(nodes)
        if(length == 0):
            raise Exception()
        for top in reversed(nodes):
            if(isinstance(top, GroupBlock)): #cripes!  It is shallow testing! Good in a way.
                break            
            if(isinstance(top, Block)):
                break
        return top

    def can_transfer(self, node, srcCoord, dstCoord):
        #boundary check
        if(dstCoord[0] < 0 or dstCoord[0] > self.col_count - 1):
            return False
        if(dstCoord[1] < 0 or dstCoord[1] > self.row_count - 1):
            return False
        #destination check
        #top = self.get_top_at(dstCoord)
        top = self.get_top_block_at(dstCoord)
        if(not top.has_vacancy()):
           return False
       #good to go
        return True
        
    def transfer(self, node, srcCoord, dstCoord):
       if(not self.can_transfer(node, srcCoord, dstCoord)):
           return False
       #else
       #
       srcNodes = self.get_nodes_at(srcCoord)
       #srcNodes.remove(node)
       pop_node(srcNodes, node)
       #
       dstNodes = self.get_nodes_at(dstCoord)
       #top = dstNodes[len(dstNodes)-1]
       push_node(dstNodes, node)
       #
       brain = node.get_brain()
       if(brain != None):
           brain.set_coord(dstCoord)
        
    def create_avatar(self, name):
        text = "[" + name + "()]"
        coord = [0, self.row_count - 1] #maybe the grid should use Y up also. :(
        nodes = self.get_nodes_at(coord)
        node = self.builder.produce(text, coord, nodes)
        brain = node.get_brain()
        if(brain == None):
           raise Exception("This node has no brain!")
        #nodes = self.get_nodes_at(0,0)
        #nodes.append(node)
        return brain
    
    def draw(self, graphics):
        self.draw_background(graphics)
        #
        glPushMatrix()
        #
        glTranslatef(graphics.x, graphics.y, graphics.z)
        #
        self.draw_rows(graphics)
        #
        #self.draw_bubbles(graphics)        
        self.bubbles.draw(graphics)
        #
        #
        glPopMatrix()
        #
        #self.draw_foreground(graphics) #not yet ...
        self.dash.draw(graphics)
        #self.draw_mice(graphics)
        self.mice.draw(graphics)

    def draw_background(self, graphics):
        bgWidth = self.bgImg.width
        bgHeight = self.bgImg.height
        
        blitY = 0
        #while(blitY < graphics.get_height()):
        while(blitY < self.window.height):
            blitX = 0
            #while(blitX < graphics.get_width()):    
            while(blitX < self.window.width):
                self.bgImg.blit(blitX, blitY, 0)
                blitX = blitX + bgWidth
            blitY = blitY + bgHeight
                    
    def draw_rows(self, graphics):
        g = graphics.copy()
        blitY = ( (self.row_count-1) * BLOCK_ROW_HEIGHT)
        for row in self.rows:
            blitX = 0
            for nodes in row:
                blitUp = 0                                    
                for node in nodes:
                    vu = node.get_vu()
                    if(vu != None):
                        #vu.draw([blitX, blitY + blitUp, 0])
                        g.translate(blitX, blitY + blitUp)
                        vu.draw(g) 
                        blitUp = blitUp + vu.get_stack_height()
                        
                blitX = blitX + BLOCK_WIDTH
            blitY = blitY - BLOCK_ROW_HEIGHT
    '''
    Bubbles:  short term hack?
    '''
    '''
    This will get the transform of a group member
    '''
    def get_member_transform(self, targetNode, coord):
        nodes = self.get_nodes_at(coord)
        blitUp = 0                                    
        for node in nodes:
            vu = node.get_vu()
            if(vu != None):
                blitUp = blitUp + vu.get_stack_height()
            if(node == targetNode):
                break
                        
        blitY = ((self.row_count - 1) * BLOCK_ROW_HEIGHT) -  (coord[1] * BLOCK_ROW_HEIGHT)
        t = [coord[0] * BLOCK_WIDTH, blitY + blitUp, 0]
        return t
    '''
    This will get the transform of any block.
    '''    
    def get_block_transform(self, block, coord):
        nodes = self.get_nodes_at(coord)
        blitUp = 0                                    
        for node in nodes:
            if(node == block):
                break
            vu = node.get_vu()
            if(vu != None):
                blitUp = blitUp + vu.get_stack_height()        
        blitY = ((self.row_count - 1) * BLOCK_ROW_HEIGHT) -  (coord[1] * BLOCK_ROW_HEIGHT)
        t = [coord[0] * BLOCK_WIDTH, blitY + blitUp, 0]
        return t
    '''
    Oh the pain ...
    '''
    def coord_to_transform(self,coord):
        nodes = self.get_nodes_at(coord)
        blitUp = 0                                    
        for node in nodes:
            vu = node.get_vu()
            if(vu != None):
                blitUp = blitUp + vu.get_stack_height()        
        blitY = ((self.row_count - 1) * BLOCK_ROW_HEIGHT) -  (coord[1] * BLOCK_ROW_HEIGHT)
        t = [coord[0] * BLOCK_WIDTH, blitY + blitUp, 0]
        return t
    '''
    def add_bubble(self, bubble):
        brain = bubble.brain
        coord = brain.get_coord()
        t = self.coord_to_transform(coord)
        t[0] += brain.node.vu.width
        bubble.set_transform(t)
        self.bubbles.append(bubble)
    '''
    def add_bubble(self, bubble):
        #self.bubbles.append(bubble)
        self.bubbles.add_node(bubble)
    
    def remove_bubble(self, bubble):
        #self.bubbles.remove(bubble)
        self.bubbles.remove_node(bubble)
    '''    
    def draw_bubbles(self, graphics):
        g = graphics.copy()
        for bubble in self.bubbles:
            vu = bubble.vu
            if(vu != None):
                t = bubble.get_transform()
                g.translate(t[0], t[1])
                #vu.draw([t[0], t[1], 0])
                vu.draw(g)
    '''
    '''
    Mouse Support
    '''
    def add_mouse(self, mouse):
        #self.mice.append(mouse)
        self.mice.add_node(mouse)
        
    def remove_mouse(self, mouse):
        #self.mice.remove(mouse)
        self.mice.remove_node(mouse)
    '''
    def draw_mice(self, graphics):
        g = graphics.copy() #fixme:necessary?
        for mouse in self.mice:                
            vu = mouse.vu
            g.x = mouse.x
            g.y = mouse.y - vu.height #fixme:mouse.hotx & hoty!!!
            vu.draw(g)
    '''