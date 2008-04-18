'''
import os, sys
import zipfile
import xml.dom.minidom

import data
'''
import graphics
import camera
from node import *
from world import *
from layer import *
from dash import *
from mouse import Mouse

from pyglet.gl import *

class Clip(graphics.Clip):
    def __init__(self, world, rowCount = 3, colCount = 3):
        super(Clip, self).__init__()
        self.world = world
        self.data = []
        self.gridX = 0
        self.gridY = 0        
        self.rowCount = rowCount
        self.colCount = colCount
        #
        self.clear_cache()

    def clear_cache(self):
        self.data = []
        i = 0
        while i < self.rowCount:
            self.data.append([None] * self.colCount)
            i += 1

    def cache_miss(self, colNdx, rowNdx):
        #print 'gridX: ' + str(gridX),' gridY:  ' + str(gridY)
        #print 'rowNdx: ' + str(rowNdx),' colNdx:  ' + str(colNdx)        
        self.data[rowNdx][colNdx] = self.world.get_grid(self.gridX + colNdx, self.gridY + rowNdx)

    def validate(self):
        #super(Clip, self).validate()
        gridColMax = self.world.gridColMax
        gridRowMax = self.world.gridRowMax
        gridWidth = gridColMax * BLOCK_WIDTH
        invGridWidth = 1. / gridWidth 
        gridHeight = gridRowMax * BLOCK_ROW_HEIGHT
        invGridHeight = 1. / gridHeight        
        #
        gridX = int(self.x * invGridWidth)
        if gridX < 0:
            gridX = 0
        gridY = int(self.y * invGridHeight)
        if gridY < 0:
            gridY = 0        
        #
        if self.gridX != gridX or self.gridY != gridY:
            self.clear_cache()
            self.gridX = gridX 
            self.gridY = gridY

class Camera(camera.Camera):
    def __init__(self, scene, rowCount = 3, colCount = 3):
        super(Camera, self).__init__()
        #
        self.world = scene.node
        self.graphics.camera = self
        clip = Clip(self.world, rowCount, colCount)
        self.clip = clip
        self.graphics.clip = clip 
        
    def validate(self):
        super(Camera, self).validate()
        self.clip.validate()

class Scene(Vu):
    
    def __init__(self, world, app, win):
        super(Scene, self).__init__(world)
        #
        self.app = app
        self.window = win
        #
        self.bgImg = image.load(data.filepath('image/clouds.jpg'))
        #
        self.bubbles = BubbleLayer(self)
        #
        self.dash = Dash(self)
        #
        self.widgets = WidgetLayer(self)
        #
        self.mice = MouseLayer(self)
    
    def create_camera(self):
        camera = Camera(self)
        return camera
    '''
    Rendering
    '''
    def draw(self, layerGraphics, worldGraphics):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #        
        self.draw_background(layerGraphics)
        #
        self.draw_world(worldGraphics)
        #
        self.dash.draw(layerGraphics)
        #
        self.widgets.draw(layerGraphics)        
        #
        self.mice.draw(layerGraphics)

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
    
    def draw_world(self, graphics):
        glPushMatrix()
        #
        glScalef(graphics.scaleX, graphics.scaleY, graphics.scaleZ)
        glTranslatef(-graphics.camera.x, -graphics.camera.y, -graphics.camera.z)        
        #
        self.draw_grids(graphics)
        #
        self.bubbles.draw(graphics)
        #
        glPopMatrix()


    def draw_grids(self, graphics):
        clip = graphics.clip
        g = graphics
        query = g.query 
        #
        gridColMax = self.node.gridColMax
        gridRowMax = self.node.gridRowMax
        #
        gridWidth = gridColMax * BLOCK_WIDTH
        invGridWidth = 1. / gridWidth 
        gridHeight = gridRowMax * BLOCK_ROW_HEIGHT
        invGridHeight = 1. / gridHeight
        #
        '''
        topPadding = gridHeight
        bottomPadding = gridHeight
        leftPadding = gridWidth
        rightPadding = gridWidth
        '''
        topPadding = 0
        bottomPadding = 0
        leftPadding = 0
        rightPadding = 0                
        #
        posX = clip.gridX * gridWidth
        posY = clip.gridY * gridHeight
        #
        bottom = clip.bottom - posY
        top = clip.top - posY
        left = clip.left - posX
        right = clip.right - posX
        #
        rowCount = clip.rowCount
        rowMax = rowCount - 1 
        colCount = clip.colCount
        colMax = colCount - 1
        #
        r1 = int(top * invGridHeight)
        if(r1 < 0):
            r1 = 0
        if(r1 > rowMax):
            r1 = rowMax
        #  
        r2 = int(bottom * invGridHeight)
        if(r2 < 0):
            r2 = 0
        if(r2 > rowMax):
            r2 = rowMax
        #
        c1 = int(left * invGridWidth)
        if(c1 < 0):
            c1 = 0
        if(c1 > colMax):
            c1 = colMax          
        #  
        c2 = int(right * invGridWidth)
        if(c2 < 0):
            c2 = 0
        if(c2 > colMax):
            c2 = colMax
        #
        r = r1
        while(r >= r2): #rows in sheet
            row = clip.data[r]
            if len(row) == 0:
                c += 1
                continue
            c = c1
            blitY = posY + (r * gridHeight)
            while(c <= c2): #cells in row
                blitX = posX + (c * gridWidth)
                grid = row[c]
                if not grid:
                    #c += 1
                    clip.cache_miss(c, r)
                    continue
                #else
                self.draw_grid(grid, g, blitX, blitY, g.z)
                c += 1
            r -= 1
        #
        #glPopMatrix()    
    
    def draw_grid(self, grid, graphics, tX, tY, tZ = 1.):
        g = graphics.copy()
        #
        glPushMatrix()
        glTranslatef(tX, tY, tZ)
        #
        g.translate(tX, tY, tZ)
        grid.vu.draw(g)
        #
        glPopMatrix()
        
    '''
    Bubbles:
    '''
    def add_bubble(self, bubble):
        self.bubbles.add_node(bubble)
    
    def remove_bubble(self, bubble):
        self.bubbles.remove_node(bubble)
    '''
    Widgets:
    '''
    def add_widget(self, widget):
        self.widgets.add_node(widget)
    
    def remove_widget(self, widget):
        self.widgets.remove_node(widget)
    '''
    Mouse Support
    '''
    def add_mouse(self, mouse):
        self.mice.add_node(mouse)
        
    def remove_mouse(self, mouse):
        self.mice.remove_node(mouse)

