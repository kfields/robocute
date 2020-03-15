import os, sys
import zipfile
import xml.dom.minidom

import data
from robocute.world import *

from robocute.builder import compile_ctors

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
    def __init__(self, filename, app, grid):
        self.filename = filename
        self.app = app        
        self.grid = grid
        #self.m_odf = zipfile.ZipFile(filename)
        self.m_odf = data.load_zip(filename)
        self.filelist = self.m_odf.infolist()
        #
        ostr = self.m_odf.read('content.xml')
        self.content = xml.dom.minidom.parseString(ostr)
            
    def read(self):
        self.read_sheets()
        self.grid.rows.reverse() #need to reverse to match OpenGL coordinate system.
        
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
        self.rowCount = len(rows)
        rowMax = self.grid.rowCount - 1        
        rowNdx = 0
        for row in rows:
            rowNdx = self.read_row(row, rowNdx, rowMax)
            if rowNdx > rowMax:
                break            

    def read_row(self, row, rowNdx, rowMax):
        grid = self.grid
        repCountStr = row.getAttributeNS(OD_TABLE_NS, 'number-rows-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        while(repCount > 0):
            gridRow = self.read_cells(row, rowNdx)
            grid.rows.append(gridRow)
            repCount = repCount - 1
            #
            if rowNdx > rowMax:
                break            
            rowNdx += 1
            
        return rowNdx            
            
    #WORLD_GRID_ROW_MAX = 64
    #WORLD_GRID_COL_MAX = 64

    def read_cells(self, row, rowNdx):
        gridRow = self.grid.create_row()
        cells = row.getElementsByTagNameNS(OD_TABLE_NS, 'table-cell')
        colNdx = 0
        colMax = self.grid.colCount - 1        
        for cell in cells:
            colNdx = self.read_cell(cell, gridRow, colNdx, colMax)
            if colNdx > colMax:
                break            
        #prevent underage
        gridRow.validate()
        return gridRow
        
    def read_cell(self, cell, gridRow, colNdx, colMax):
        grid = self.grid
        repCountStr = cell.getAttributeNS(OD_TABLE_NS, 'number-columns-repeated')
        if(repCountStr == ''):
            repCount = 1
        else:
            repCount = int(repCountStr)
        cellTxt = get_text(cell)
                
        while(repCount > 0):
            cell = gridRow.create_cell()
            cell.ctors = compile_ctors(cellTxt)
            gridRow.append(cell)
            repCount = repCount - 1
            #
            if colNdx > colMax:
                break            
            colNdx += 1
            
        return colNdx
            
