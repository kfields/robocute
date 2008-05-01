
import pyglet
import data

from robocute.graphics import *
from robocute.quad import *
from robocute.shape import Rect

GRID_SW = 0
GRID_SC = 1
GRID_SE = 2
GRID_CW = 3
GRID_CC = 4
GRID_CE = 5
GRID_NW = 6
GRID_NC = 7
GRID_NE = 8

class SkinData(object):
    def __init__(self, sliceCount):
        self.sliceCount = sliceCount
        self.slices = [None] * sliceCount

class FileSkinData(SkinData):
    def __init__(self, slicesName, sliceCount):
        super(FileSkinData, self).__init__(sliceCount)
        self.atlas = pyglet.image.atlas.TextureAtlas()
        
        imgCount = 0        
        while(imgCount != sliceCount):
            slice = self.load_slice(slicesName + '_0' + str(imgCount+1) + '.png')
            self.slices[imgCount] = slice
            imgCount += 1
            
        self.texture = self.atlas.texture

    def load_slice(self, filename):
        image = pyglet.image.load(data.filepath('image/skin/' + filename))
        slice = self.atlas.add(image)
        return slice

class GridSkinner(SkinData):
    def __init__(self, filename, cornerWidth = 32, cornerHeight = 32):
        super(GridSkinner, self).__init__(9)
        image = pyglet.image.load(data.filepath('image/skin/' + filename + '.png'))
        texture = image.get_texture(True)
        self.texture = texture
        width = texture.width  
        height = texture.height
        slices = self.slices
        rowHeights = [cornerHeight, height - cornerHeight * 2, cornerHeight]
        colWidths = [cornerWidth, width - cornerWidth * 2, cornerWidth]
        i = 0
        sliceY = 0
        while i < 3:
            j = 0
            sliceX = 0
            sliceHeight = rowHeights[i]            
            while j < 3:
                sliceWidth = colWidths[j]
                slices[i * 3 + j] = texture.get_region(sliceX, sliceY, sliceWidth, sliceHeight)
                sliceX += sliceWidth
                j += 1
            sliceY += sliceHeight
            i += 1 
         
                
class Skin(object):
    def __init__(self, data):
        self.data = data
        self.content = Rect()
        self.margin_top = 5
        self.margin_bottom = 5        
        self.margin_left = 5
        self.margin_right = 5        
        #
        self.validate()

    def validate(self):
        pass
    
    def draw(self, graphics):
        pass

class HorizontalSkin(Skin):
    def __init__(self, data):
        super(HorizontalSkin, self).__init__(data)

    def validate(self):
        slices = self.data.slices
        self.margin_left = slices[0].width
        self.margin_right = slices[2].width
        #
        self.content.width = slices[1].width
        self.content.height = slices[1].height

    def compose(self, graphics):
        slices = self.data.slices
        mesh = QuadMesh(self.data.texture)
        quads = QuadRow()
        #home slice
        quads.add_quad(Quad(slices[0]))
        #fill slice
        fillWidth = graphics.width - self.margin_left - self.margin_right
        fillCount = fillWidth / slices[1].width 
        fillModulo = fillWidth % slices[1].width
        i = 0
        while i < fillCount:
            quads.add_quad(Quad(slices[1]))
            i += 1
        if fillModulo:
            quad = Quad(slices[1])
            quad.width = fillModulo 
            quads.add_quad(quad)
        #end slice
        quads.add_quad(Quad(slices[2]))
        #    
        quads.compose(graphics, mesh)
        return mesh
    
    def draw(self, graphics):
        mesh = self.compose(graphics)
        mesh.draw()
        
class VerticalSkin(Skin):
    def __init__(self, data):
        super(VerticalSkin, self).__init__(data)

    def validate(self):
        slices = self.data.slices
        self.margin_bottom = slices[0].height
        self.margin_top = slices[2].height
        #
        self.content.width = slices[1].width
        self.content.height = slices[1].height

    def compose(self, graphics):
        slices = self.data.slices
        mesh = QuadMesh(self.data.texture)
        quads = QuadColumn()
        #home slice
        quads.add_quad(Quad(slices[0]))
        #fill slice
        fillHeight = graphics.height - self.margin_bottom - self.margin_top
        fillCount = fillHeight / slices[1].height 
        fillModulo = fillHeight % slices[1].height
        i = 0
        while i < fillCount:
            quads.add_quad(Quad(slices[1]))
            i += 1
        if fillModulo:
            quad = Quad(slices[1])
            quad.height = fillModulo 
            quads.add_quad(quad)
        #end slice
        quads.add_quad(Quad(slices[2]))
        #    
        quads.compose(graphics, mesh)
        return mesh
            
    def draw(self, graphics):
        mesh = self.compose(graphics) 
        mesh.draw()
        
class GridSkin(Skin):
    def __init__(self, data):
        super(GridSkin, self).__init__(data)

    def validate(self):
        slices = self.data.slices
        self.margin_left = slices[GRID_SW].width
        self.margin_right = slices[GRID_SE].width
        self.margin_bottom = slices[GRID_SW].height
        self.margin_top = slices[GRID_NW].height        
        #
        self.content.width = slices[GRID_CC].width
        self.content.height = slices[GRID_CC].height
        
    def compose(self, graphics):
        slices = self.data.slices
        mesh = QuadMesh(self.data.texture)
        grid = QuadGrid()
        #footer
        footer = self.create_footer(graphics, grid)
        grid.add_row(footer)
        #center rows
        fillHeight = graphics.height - self.margin_bottom - self.margin_top
        fillCount = fillHeight / slices[GRID_CC].height 
        fillModulo = fillHeight % slices[GRID_CC].height
        i = 0
        while i < fillCount:
            row = self.create_center(graphics, grid)
            grid.add_row(row)
            i += 1
        if fillModulo:
            row = self.create_center(graphics, grid)
            row.height = fillModulo 
            grid.add_row(row)
        #end row
        header = self.create_header(graphics, grid)
        grid.add_row(header)
        #    
        grid.compose(graphics, mesh)
        return mesh
            
    def create_header(self, graphics, grid):
        return self.create_row(graphics, grid, 6)

    def create_center(self, graphics, grid):
        return self.create_row(graphics, grid, 3)

    def create_footer(self, graphics, grid):
        return self.create_row(graphics, grid, 0)
        
    def create_row(self, graphics, grid, sliceNdx):
        slices = self.data.slices
        quads = QuadRow()
        #home slice
        quads.add_quad(Quad(slices[sliceNdx + 0]))
        #fill slice
        fillWidth = graphics.width - self.margin_left - self.margin_right
        fillCount = fillWidth / slices[sliceNdx + 1].width 
        fillModulo = fillWidth % slices[sliceNdx + 1].width
        i = 0
        while i < fillCount:
            quads.add_quad(Quad(slices[sliceNdx + 1]))
            i += 1
        if fillModulo:
            quad = Quad(slices[sliceNdx + 1])
            quad.width = fillModulo 
            quads.add_quad(quad)
        #end slice
        quads.add_quad(Quad(slices[sliceNdx + 2]))
        #    
        return quads
    
    def draw(self, graphics):
        mesh = self.compose(graphics)
        mesh.draw()
        