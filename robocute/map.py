
from node import *

class Cell(object):
    def __init__(self):
        self.vacancy = False
        
class Map(object):
    def __init__(self, coordX, coordY, width, height):
        self.coordX = coordX
        self.coordY = coordY
        self.width = width
        self.height = height
        self.rows = []
        i = 0
        while i < self.height:
            self.rows.append([None] * self.width)
            i += 1
    
    def get_cell_at(self, x, y):
        #print 'x: ', x, 'y: ', y
        return self.rows[y][x]
    
    def set_cell_at(self, x, y, cell):
        #print 'x: ', x, 'y: ', y
        self.rows[y][x] = cell
    
class Explorer(object):
    def __init__(self, map, callback):
        self.map = map
        self.callback = callback
         
    def explore(self, x, y):
        map = self.map
        #
        #cell = self.callback(Coord(x, y))
        cell = self.callback(Coord(map.coordX + x, map.coordY + y))
        map.set_cell_at(x, y, cell)
        #
        if(not cell.vacancy):
            return
        #else
        #explore north
        if(y != map.height - 1):
            cell = map.get_cell_at(x, y+1)
            if(not cell):
                self.explore(x, y+1)
        #explore east
        if(x != map.width - 1):
            cell = map.get_cell_at(x+1, y)
            if(not cell):
                self.explore(x+1, y)
        #explore south
        if(y != 0):
            cell = map.get_cell_at(x, y-1)
            if(not cell):
                self.explore(x, y-1)
        #explore west
        if(x != 0):
            cell = map.get_cell_at(x-1, y)
            if(not cell):
                self.explore(x-1, y)
