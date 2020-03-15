import os, sys
import zipfile
import xml.dom.minidom

import data

from robocute.catalog import *

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
DNDX_TITLE = 3 
DNDX_IMG = 5
DNDX_SEQ = 7
DNDX_EXTRA = DNDX_SEQ + 1
 
class Reader(object):
    
    def __init__(self, catalog, filename):
        self.catalog = catalog
        self.page = None
        self.filename = filename
        #self.m_odf = zipfile.ZipFile(filename)
        self.m_odf = data.load_zip(filename)
        self.filelist = self.m_odf.infolist()
        #
        ostr = self.m_odf.read('content.xml')
        self.content = xml.dom.minidom.parseString(ostr)
            
    def read(self):
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
        page = self.create_page(self.sheet_name, items)
        self.catalog.add_page(self.sheet_name, page)
        
    def read_rows(self, sheet, items):
        rows = sheet.getElementsByTagNameNS(OD_TABLE_NS, 'table-row')
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
        if datum == 'item' or datum == 'tool':
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
        ndx = DNDX_EXTRA
        assignments = []
        while ndx < len(data):
            prop = data[ndx]
            if prop == '':
                break
            val = data[ndx+1]
            assignments.append( ( prop, eval(val) ) )
            ndx += 2
        item = self.catalog.create_item(data[DNDX_PROP], data[DNDX_VAL], data[DNDX_TITLE], data[DNDX_IMG], data[DNDX_SEQ], assignments)            
        return item
