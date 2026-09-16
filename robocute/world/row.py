from typing import TYPE_CHECKING

from robocute.base import *
if TYPE_CHECKING:
    from .grid import Grid
from .cell import *


class Row(list):
    def __init__(self, grid: "Grid"):
        super().__init__()
        self.grid = grid
        self.col_count = grid.col_count
        self.invalid = 0

    def invalidate(self, flag=1):
        if self.invalid == 0:
            self.grid.invalidate()
        self.invalid |= flag

    def validate(self):
        self.invalid = 0
        # prevent underage
        data = self
        if len(data) < self.col_count:
            i = 0
            while i < self.col_count:
                data.append(self.create_cell())
                i += 1
        for cell in self:
            if cell.invalid != 0:
                cell.validate()

    def create_cell(self):
        cell = Cell(self)
        return cell

    def build(self, app, grid, rowNdx):
        self.grid = grid
        colNdx = 0
        for cell in self:
            coord = Coord(self.grid.coordX + colNdx, self.grid.coordY + rowNdx)
            cell.build(app, self, coord)
            colNdx += 1

    def clone(self):
        clone = Row(self.grid)
        for cell in self:
            cloneCell = cell.clone()
            clone.append(cloneCell)
        return clone
