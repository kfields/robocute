'''
import os, sys
import zipfile
import xml.dom.minidom

import data
'''
import camera
from node import *
from world import *
from layer import *
from dash import *
from mouse import Mouse

from pyglet.gl import *

class Camera(camera.Camera):
    def __init__(self, scene):
        super(Camera, self).__init__(scene)
        self.rowCount = 3
        self.colCount = 3
        #self.data = [[None] * self.colCount ] * self.rowCount
        self.data = []
        i = 0
        while i < self.rowCount:
            self.data.append([None] * self.colCount)
            i += 1
        
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
    def draw(self, graphics, camera):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #        
        self.draw_background(graphics)
        #
        self.draw_world(camera)
        #
        self.dash.draw(graphics)
        #
        self.widgets.draw(graphics)        
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
    
    def draw_world(self, camera):
        glPushMatrix()
        #
        glTranslatef(-camera.x, -camera.y, -camera.z)
        glScalef(camera.scaleX, camera.scaleY, camera.scaleZ)        
        #
        #self.node.grid.vu.draw(camera)
        self.draw_grids(camera)
        #
        self.bubbles.draw(camera)
        #
        glPopMatrix()

    '''
    WORLD_GRID_WIDTH = WORLD_GRID_COL_MAX * BLOCK_WIDTH
    WORLD_GRID_HEIGHT = WORLD_GRID_ROW_MAX * BLOCK_ROW_HEIGHT
    WORLD_GRID_CACHE_WIDTH = WORLD_GRID_CACHE_COL_COUNT * WORLD_GRID_WIDTH
    WORLD_GRID_CACHE_HEIGHT = WORLD_GRID_CACHE_ROW_COUNT * WORLD_GRID_HEIGHT
    '''

    def draw_grids(self, camera):
        #g = camera.copy()
        g = camera
        query = g.query 
        #
        invScaleX = 1. / g.scaleX
        invScaleY = 1. / g.scaleY
        invScaleZ = 1. / g.scaleZ
        #
        gridWidth = self.node.gridColMax * BLOCK_WIDTH
        invGridWidth = 1. / gridWidth 
        gridHeight = self.node.gridRowMax * BLOCK_ROW_HEIGHT
        invGridHeight = 1. / gridHeight
        #
        width = int((g.width + BLOCK_WIDTH) * invScaleX)
        height = int((g.height + BLOCK_ROW_HEIGHT) * invScaleY)
        bottom = int((g.y - BLOCK_ROW_HEIGHT) * invScaleY)
        top = bottom + height
        left = int((g.x - BLOCK_WIDTH) * invScaleX)
        right = left + width
        #
        rowCount = camera.rowCount
        rowMax = rowCount - 1 
        colCount = camera.colCount
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
            row = camera.data[r]
            if len(row) == 0:
                c += 1
                continue
            c = c1
            blitY = r * gridHeight
            while(c <= c2): #cells in row
                blitX = c * gridWidth                
                grid = row[c]
                if not grid:
                    #c += 1
                    self.cache_miss(camera, r, c)
                    continue
                #else
                self.draw_grid(grid, camera, blitX, blitY, camera.z)
                c += 1
            r -= 1            
    
    def cache_miss(self, camera, rowNdx, colNdx):
        camera.data[rowNdx][colNdx] = self.node.get_grid(colNdx, rowNdx)
        
    def draw_grid(self, grid, camera, tX, tY, tZ = 1.):
        g = camera
        #
        glPushMatrix()
        glTranslatef(tX, tY, tZ)
        #
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

