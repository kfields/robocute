from loguru import logger

from crunge.engine.d2 import Node2D

from robocute.node import *
from robocute.block import *

from .cell import *
from .row import *

from crunge.engine.vu_group import VuGroup
from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup
from crunge.engine.d2.sprite.instanced.instanced_sprite_vu_group import (
    InstancedSpriteVuGroup,
)


class Grid(GameNode):
    def __init__(self, col_count=WORLD_GRID_COL_MAX, row_count=WORLD_GRID_ROW_MAX, is_template: bool = False):
        super().__init__()
        logger.debug(f"Initializing Grid with col_count: {col_count}, row_count: {row_count}, is_template: {is_template}")
        #
        self.col_count = col_count
        self.row_count = row_count
        self.rows = []

        self.sprite_group = DynamicSpriteGroup(1024).enable()
        self.vu_group = self.add(InstancedSpriteVuGroup(1024, self.sprite_group))
        self.dirty = True
        self.is_template = is_template

    def mark_dirty(self) -> None:
        self.dirty = True

    def get_vu_group(self, vu_type: type = None) -> VuGroup | None:
        return self.vu_group

    def on_child_added(self, child):
        super().on_child_added(child)
        self.mark_dirty()
        #Scheduler().schedule_once(self.rebuild)

    def rebuild(self, delta_time: float):
        self.vu_group.clear()
        for row in reversed(self.rows):
            for cell in row:
                for node in cell:
                    vu = node.vu
                    #logger.debug(f"node class: {type(node)}: {node.is_enabled}")
                    if vu is not None:
                        #logger.debug(f"vu class: {type(vu)}: {vu}")
                        #logger.debug(f"vu class: {type(vu)}: {vu}, position: {vu.node.position}")
                        if not isinstance(vu, SpriteVu):
                            continue
                        if not vu.is_enabled:
                            raise ValueError(f"Vu is not enabled: {vu}")

                        self.vu_group.append(vu)

    def _update(self, delta_time: float):
        if self.dirty and self.is_ready:
        #if self.dirty:
            self.rebuild(delta_time)
            self.dirty = False
        super()._update(delta_time)

    def validate(self):
        super().validate()
        # prevent underage
        rows = self.rows
        if len(rows) < self.row_count:
            i = 0
            while i < self.row_count:
                row = self.create_row()
                row.validate()
                rows.append(row)
                i += 1
        for row in self.rows:
            if row.invalid != 0:
                row.validate()

    def create_row(self):
        row = Row(self)
        return row

    def build(self, app, world, x, y):
        self.world = world
        self.gridX = x
        self.gridY = y
        self.coordX = x * self.col_count
        self.coordY = y * self.row_count

        if not self.is_template:
            world.add_grid(self)

        # prevent underage
        self.validate()
        
        #
        rowNdx = 0
        for row in self.rows:
            row.build(app, self, rowNdx)
            rowNdx += 1

    def clone(self):
        clone = Grid(self.col_count, self.row_count)
        for row in self.rows:
            cloneRow = row.clone()
            clone.rows.append(cloneRow)
        return clone

    def valid_coord(self, coord):
        """
        if coord.x < 0 or coord.x > self.coordX + self.colCount - 1:
            return False
        if coord.y < 0 or coord.y > self.coordY + self.rowCount - 1:
            return False
        """
        if coord.x < 0 or coord.y < 0:
            return False

        return True

    def is_local_coord(self, coord) -> bool:
        if coord.x < self.coordX or coord.x > self.coordX + self.col_count - 1:
            return False
        if coord.y < self.coordY or coord.y > self.coordY + self.row_count - 1:
            return False
        return True

    def to_local_coord(self, coord) -> Coord:
        return Coord(coord.x % self.col_count, coord.y % self.row_count)

    def get_cell_at(self, coord) -> Cell:
        """
        if(not self.valid_coord(coord)):
            raise Exception('Invalid Coordinates: x: ', coord.x, ' y: ', coord.y)
        """
        if not self.is_local_coord(coord):
            return self.world.get_cell_at(coord)
        # else
        return self.rows[coord.y % self.row_count][coord.x % self.col_count]

    """
    Cell Access Helpers
    """

    def get_top_at(self, coord):
        cell = self.get_cell_at(coord)
        top = cell.get_top()
        return top

    def get_top_block_at(self, coord):
        cell = self.get_cell_at(coord)
        top = cell.get_top_block()
        return top

    def get_top_transform_at(self, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_top_transform(coord)
        return t

    def get_bottom_transform_at(self, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_bottom_transform(coord)
        return t

    """
    This will get the transform of a group member
    """

    def get_node_transform_at(self, targetNode, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_node_transform(targetNode, coord)
        return t

    """
    This will get the transform of any block.
    """

    def get_block_transform_at(self, block, coord):
        cell = self.get_cell_at(coord)
        t = cell.get_block_transform(block, coord)
        return t
