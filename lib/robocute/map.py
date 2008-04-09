class Cell(object):
    def __init__(self):
        self.explored = True
        self.vacancy = False
        
class Map(object):
    def __init__(self, width, height):
        self.width = width  
        self.height = height
        self.rows = [ [ None ] * width ] * height #produces same instance!!! Bad.                
    
    def cell_at(self, x, y):
        #print 'x: ', x, 'y: ', y
        return self.rows[y][x]
    
class Explorer(object):
    def __init__(self, map, callback):
        self.map = map
        self.callback = callback
         
    def explore(self, x, y):
        map = self.map
        #
        cell = self.callback(x, y)
        #
        if(not cell.vacancy):
            return
        #else
        #explore north
        if(y != map.height - 1):
            cell = map.cell_at(x, y+1)
            if(not cell):
                self.explore(x, y+1)
        #explore east
        if(x != map.width - 1):
            cell = map.cell_at(x+1, y)
            if(not cell):
                self.explore(x+1, y)
        #explore south
        if(y != 0):
            cell = map.cell_at(x, y-1)
            if(not cell):
                self.explore(x, y-1)
        #explore west
        if(x != 0):
            cell = map.cell_at(x-1, y)
            if(not cell):
                self.explore(x-1, y)
