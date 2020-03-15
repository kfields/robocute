
from robocute.base import *
from .cell import *

class Row(list):
    def __init__(self, colCount = WORLD_GRID_COL_MAX):
        super(Row, self).__init__()
        self.colCount = colCount
        self.invalid = 0
        
    def invalidate(self, flag = 1):
        if self.invalid == 0:
            self.grid.invalidate()
        self.invalid |= flag
       
    def validate(self):
        self.invalid = 0
        #prevent underage
        data = self
        if len(data) < self.colCount:
            i = 0
            while i < self.colCount:
                data.append(self.create_cell())
                i += 1
        for cell in self:
            if cell.invalid != 0:            
                cell.validate()

    def create_cell(self):
        cell = Cell()
        return cell

    def build(self, app, grid, rowNdx):
        self.grid = grid        
        colNdx = 0
        for cell in self:
            coord = Coord(self.grid.coordX + colNdx, self.grid.coordY + rowNdx)
            cell.build(app, self, coord)
            colNdx += 1

    def clone(self):
        clone = Row(self.colCount)
        for cell in self:
            cloneCell = cell.clone()
            clone.append(cloneCell)
        return clone
