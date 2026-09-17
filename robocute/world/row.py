from typing import TYPE_CHECKING, Iterator

from robocute.base import *

if TYPE_CHECKING:
    from .grid import Grid

from .cell import *


class Row(list):
    """One row of cells, left to right.

    Cells are filled in by `validate`, so a freshly constructed Row is empty
    and a cloned one is filled by the clone loop instead.
    """

    def __init__(self, grid: "Grid"):
        super().__init__()
        self.grid = grid
        self.col_count = grid.col_count
        self.invalid = 0

    def __repr__(self) -> str:
        return f"Row({len(self)} cells)"

    def clone(self, grid: "Grid") -> "Row":
        """Copy this row's cells onto a new grid.

        The target grid is passed explicitly: cells resolve `cell.grid` through
        `cell.row.grid`, so a clone bound to the source grid would register its
        nodes on the template.
        """
        clone = Row(grid)
        for cell in self:
            clone.append(cell.clone(clone))
        return clone

    # ------------------------------------------------------------------
    # Visuals
    # ------------------------------------------------------------------

    def yield_visuals(self) -> Iterator:
        """Yield the vus of this row, left to right, each cell bottom to top."""
        for cell in self:
            yield from cell.yield_visuals()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def invalidate(self, flag=1):
        if self.invalid == 0:
            self.grid.invalidate()
        self.invalid |= flag

    def validate(self):
        self.invalid = 0
        # prevent underage
        while len(self) < self.col_count:
            self.append(self.create_cell())

        for cell in self:
            if cell.invalid != 0:
                cell.validate()

    def create_cell(self) -> Cell:
        return Cell(self)

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, app, grid: "Grid", row_ndx: int):
        self.grid = grid
        for col_ndx, cell in enumerate(self):
            coord = Coord(
                self.grid.coordX + col_ndx,
                self.grid.coordY + row_ndx,
            )
            cell.build(app, coord)
