from loguru import logger

from crunge.engine.d2 import Node2D

from robocute.node import *
from robocute.block import *

from .cell import *
from .row import *

from crunge.engine.vu_group import VuGroup
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup
from crunge.engine.d2.sprite.instanced.instanced_sprite_vu_group import (
    InstancedSpriteVuGroup,
)


class Grid(Node):
    def __init__(self, colCount=WORLD_GRID_COL_MAX, rowCount=WORLD_GRID_ROW_MAX):
        super().__init__()
        #
        self.colCount = colCount
        self.rowCount = rowCount
        self.rows = []

        self.sprite_group = DynamicSpriteGroup(1024).enable()
        # self.vu_group = self.add(InstancedSpriteVuGroup(1024, self.sprite_group))
        #self.dirty = True
        self.dirty = False

    def _seat(self):
        super()._seat()
        self.vu_group = self.add(InstancedSpriteVuGroup(1024, self.sprite_group))

    def get_vu_group(self, vu_type: type = None) -> VuGroup | None:
        return self.vu_group

    def on_child_added(self, child):
        super().on_child_added(child)
        vu = child.vu
        '''
        if vu is not None:
            self.vu_group.append(vu)
        '''
        self.dirty = True
        # Scheduler().schedule_once(self.rebuild)

    def rebuild(self, delta_time: float):
        self.vu_group.clear()
        for row in reversed(self.rows):
            for cell in row:
                for node in cell:
                    vu = node.vu
                    #logger.debug(f"node class: {type(node)}: {node.is_enabled}")
                    if vu is not None:
                        #logger.debug(f"vu class: {type(vu)}: {vu}")
                        if not isinstance(vu, SpriteVu):
                            continue
                        if not vu.is_enabled:
                            raise ValueError(f"Vu is not enabled: {vu}")
                        self.vu_group.append(vu)

    def _update(self, delta_time: float):
        if self.dirty and self.is_ready:
            self.rebuild(delta_time)
            self.dirty = False
        super()._update(delta_time)

    """
    def _update(self, delta_time: float):
        if self.dirty:
            self.vu_group.clear()
            for row in self.rows:
                for cell in row:
                    for node in cell:
                        vu = node.vu
                        if vu is not None:
                            logger.debug(f'vu class: {type(vu)}: {vu}')
                            if not isinstance(vu, SpriteVu):
                                continue
                            self.vu_group.append(vu)
            self.dirty = False
        super()._update(delta_time)
    """

    """
    def add_child(self, child):
        logger.debug(f'Adding child: {child}, enabled: {child.vu.is_enabled if child.vu is not None else False}')
        if child.vu is not None:
            exit()
            self.vu_group.append(child.vu)
        super().add_child(child)
    """

    """
    def on_child_added(self, child):
        super().on_child_added(child)
        if child.vu is not None:
            self.vu_group.append(child.vu)
        '''
        self.vu_group.clear()
        for row in self.rows:
            for cell in row:
                for node in cell:
                    vu = node.vu
                    if vu is not None:
                        self.vu_group.append(vu)
        '''
    """

    def validate(self):
        super().validate()
        # prevent underage
        rows = self.rows
        if len(rows) < self.rowCount:
            i = 0
            while i < self.rowCount:
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
        self.coordX = x * self.colCount
        self.coordY = y * self.rowCount
        # do this last!!!
        # world.add_grid(self)
        # prevent underage
        self.validate()
        #
        rowNdx = 0
        for row in self.rows:
            row.build(app, self, rowNdx)
            rowNdx += 1

    def clone(self):
        clone = Grid(self.colCount, self.rowCount)
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

    def local_coord(self, coord):
        if coord.x < self.coordX or coord.x > self.coordX + self.colCount - 1:
            return False
        if coord.y < self.coordY or coord.y > self.coordY + self.rowCount - 1:
            return False
        return True

    def to_local_coord(self, coord):
        return Coord(coord.x % self.colCount, coord.y % self.rowCount)

    def get_cell_at(self, coord):
        """
        if(not self.valid_coord(coord)):
            raise Exception('Invalid Coordinates: x: ', coord.x, ' y: ', coord.y)
        """
        if not self.local_coord(coord):
            return self.world.get_cell_at(coord)
        # else
        return self.rows[coord.y % self.rowCount][coord.x % self.colCount]

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
