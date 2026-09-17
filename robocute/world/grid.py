from typing import Iterator

from loguru import logger

from crunge.engine.d2 import Node2D
from crunge.engine.vu_group import VuGroup
from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup
from crunge.engine.d2.sprite.instanced.instanced_sprite_vu_group import (
    InstancedSpriteVuGroup,
)

from robocute.node import *
from robocute.block import *

from .cell import *
from .row import *


class Grid(GameNode):
    """A rectangular field of stacked cells, rendered as one instance stream.

    Rendering contract:

    * The grid, not the individual nodes, draws the world. Nodes carry vus but
      must not draw themselves -- a self-drawing node emits `Draw(4, 1)` with
      the group's bind group still set, which is a pipeline layout mismatch.
    * `yield_visuals` produces the total draw order: rows back to front, cells
      left to right, stacks bottom to top. Each level delegates to the next,
      bottoming out in `GameNode.yield_visuals`, so a container node such as
      GroupBlock can substitute its members' visuals for its own.
    * A vu appears exactly once in that stream. A node in two cells yields
      twice and the vu group rejects the duplicate, which is the intended
      signal that something moved without being removed from its old cell.
    """

    def __init__(
        self,
        col_count: int = WORLD_GRID_COL_MAX,
        row_count: int = WORLD_GRID_ROW_MAX,
        is_template: bool = False,
    ):
        super().__init__()
        logger.debug(
            f"Initializing Grid with col_count: {col_count}, "
            f"row_count: {row_count}, is_template: {is_template}"
        )
        self.col_count = col_count
        self.row_count = row_count
        self.rows: list[Row] = []

        self.sprite_group = DynamicSpriteGroup(1024).enable()
        self.vu_group = self.add(InstancedSpriteVuGroup(1024, self.sprite_group, is_managed=True))
        self.dirty = True
        self.is_template = is_template

    def clone(self) -> "Grid":
        clone = Grid(self.col_count, self.row_count)
        for row in self.rows:
            clone.rows.append(row.clone(clone))
        return clone

    # ------------------------------------------------------------------
    # Vu group
    # ------------------------------------------------------------------

    def get_vu_group(self, vu_type: type = None) -> VuGroup | None:
        """Claim vus created by descendants.

        A node walks up looking for this, so a block's vu is created against
        this grid's layout from the start rather than the per-model one.
        """
        return self.vu_group

    # ------------------------------------------------------------------
    # Visuals
    # ------------------------------------------------------------------

    def yield_visuals(self) -> Iterator:
        """The draw order, back to front.

        `reversed(self.rows)` assumes row 0 is nearest the viewer. If back-row
        stacks draw over front-row ones, this is the line to flip.
        """
        for row in reversed(self.rows):
            yield from row.yield_visuals()

    # ------------------------------------------------------------------
    # Rebuild
    # ------------------------------------------------------------------

    def mark_dirty(self) -> None:
        self.dirty = True

    '''
    def on_child_added(self, child):
        super().on_child_added(child)
        if not self.dirty:
            # Coalesce: a world build adds hundreds of children and only needs
            # one scheduled rebuild, not one per child.
            self.mark_dirty()
            Scheduler().schedule_once(self.rebuild)
        else:
            self.mark_dirty()
    '''

    def rebuild(self, delta_time: float = 0.0):
        group = self.vu_group
        group.clear()

        count = 0
        for vu in self.yield_visuals():
            if not isinstance(vu, SpriteVu):
                continue
            if not vu.is_enabled:
                raise ValueError(f"Vu is not enabled: {vu}")
            group.append(vu)
            count += 1

        self.dirty = False
        logger.debug(f"Grid rebuild: {count} instances")

    def rebuild_if_dirty(self, delta_time: float = 0.0) -> None:
        if self.dirty:
            self.rebuild(delta_time)

    def _ready(self):
        super()._ready()
        self.rebuild_if_dirty()

    def _draw(self):
        self.rebuild_if_dirty()
        super()._draw()

    def _update(self, delta_time: float):
        self.rebuild_if_dirty(delta_time)
        super()._update(delta_time)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self):
        super().validate()
        # prevent underage
        while len(self.rows) < self.row_count:
            row = self.create_row()
            row.validate()
            self.rows.append(row)

        for row in self.rows:
            if row.invalid != 0:
                row.validate()

    def create_row(self) -> Row:
        return Row(self)

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

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

        for row_ndx, row in enumerate(self.rows):
            row.build(app, self, row_ndx)

    # ------------------------------------------------------------------
    # Coordinates
    # ------------------------------------------------------------------

    def valid_coord(self, coord) -> bool:
        return coord.x >= 0 and coord.y >= 0

    def is_local_coord(self, coord) -> bool:
        if coord.x < self.coordX or coord.x > self.coordX + self.col_count - 1:
            return False
        if coord.y < self.coordY or coord.y > self.coordY + self.row_count - 1:
            return False
        return True

    def to_local_coord(self, coord) -> Coord:
        return Coord(coord.x % self.col_count, coord.y % self.row_count)

    def get_cell_at(self, coord) -> Cell:
        if not self.is_local_coord(coord):
            return self.world.get_cell_at(coord)
        return self.rows[coord.y % self.row_count][coord.x % self.col_count]

    # ------------------------------------------------------------------
    # Cell access helpers
    # ------------------------------------------------------------------

    def get_top_at(self, coord):
        return self.get_cell_at(coord).get_top()

    def get_top_block_at(self, coord):
        return self.get_cell_at(coord).get_top_block()

    def get_top_transform_at(self, coord):
        return self.get_cell_at(coord).get_top_transform(coord)

    def get_bottom_transform_at(self, coord):
        return self.get_cell_at(coord).get_bottom_transform(coord)

    def get_node_transform_at(self, target_node, coord):
        """Transform of a group member."""
        return self.get_cell_at(coord).get_node_transform(target_node, coord)

    def get_block_transform_at(self, block, coord):
        """Transform of any block."""
        return self.get_cell_at(coord).get_block_transform(block, coord)

    # ------------------------------------------------------------------
    # Mutation helpers -- keep callers off Cell internals
    # ------------------------------------------------------------------

    def push_node_at(self, node, coord):
        self.get_cell_at(coord).push_node(node, coord)

    def remove_node_at(self, node, coord=None):
        coord = coord if coord is not None else node.coord
        self.get_cell_at(coord).remove_node(node, coord)

    def pop_node_at(self, coord):
        return self.get_cell_at(coord).pop_node(coord)

    def move_node(self, node, coord):
        """Relocate a node to another cell.

        Removal comes first: `push_node` overwrites `node.coord`, so looking up
        the old cell afterwards finds the new one. Doing a move as a bare push
        leaves the node in both cells, and `yield_visuals` then emits its vu
        twice.
        """
        old_coord = node.coord
        if old_coord is not None:
            self.get_cell_at(old_coord).remove_node(node, old_coord)
        self.get_cell_at(coord).push_node(node, coord)
