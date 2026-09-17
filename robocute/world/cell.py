from typing import TYPE_CHECKING, Iterator

from loguru import logger
import glm

from robocute.base import *
from robocute.block import *
from robocute.builder import execute_ctors
from robocute.node import GameNode

if TYPE_CHECKING:
    from .row import Row


class Cell(list):
    """A stack of nodes at one grid coordinate.

    Index 0 is the bottom of the stack, index -1 the top. The list order IS the
    draw order within the cell.

    `yield_visuals` delegates to each node rather than reading `node.vu`
    directly, so a container node -- a GroupBlock -- can yield its members'
    visuals in place of its own. Reading `vu` here made absorbed nodes
    invisible to the renderer.

    Mutation only changes the list. Positioning and grid registration happen in
    one place, `update`, which every mutating method ends with.
    """

    def __init__(self, row: "Row" = None):
        super().__init__()
        self.row = row
        self.invalid = 0
        self.height = 0
        self.ctors = None

    def __repr__(self) -> str:
        return f"Cell({list.__repr__(self)})"

    @property
    def grid(self):
        return self.row.grid if self.row else None

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def invalidate(self, flag=1):
        if self.invalid == 0 and self.row is not None:
            self.row.invalidate()
        self.invalid |= flag

    def validate(self):
        self.invalid = 0

    # ------------------------------------------------------------------
    # Visuals
    # ------------------------------------------------------------------

    def yield_visuals(self) -> Iterator:
        """Yield the vus of this cell, bottom of the stack to top.

        Each node decides what it contributes. GameNode yields its own vu if it
        has one; GroupBlock overrides to yield from its members instead.
        """
        for node in self:
            yield from node.yield_visuals()

    # ------------------------------------------------------------------
    # Grid registration -- the only two places that touch grid children
    # ------------------------------------------------------------------

    def _attach(self, node: GameNode, coord: Coord) -> None:
        node.coord = coord
        node.grid = self.grid

        grid = self.grid
        if grid is None or grid.is_template:
            return
        if node.parent is None:
            grid.add_child(node)

    def _detach(self, node: GameNode) -> None:
        """Release a node from the grid, members first.

        Without the recursion a removed group leaves its members parented to
        the grid with live vus still holding instance slots.
        """
        for member in self._members_of(node):
            self._detach(member)

        #node.coord = None

        grid = self.grid
        if grid is None or grid.is_template:
            return
        if node.parent is not None:
            # ASSUMPTION: Node exposes remove_child. Swap if it is `remove`.
            grid.remove_child(node)

    @staticmethod
    def _members_of(node: GameNode):
        """Stack-ordered children of a container node, or an empty tuple."""
        if isinstance(node, GroupBlock):
            # ASSUMPTION: GroupBlock.nodes, bottom to top.
            return list(node.nodes)
        return ()

    # ------------------------------------------------------------------
    # Layout -- the single point of truth
    # ------------------------------------------------------------------

    def update(self, coord: Coord) -> None:
        """Recompute stack height, then position and register every node.

        Every mutating method ends here. Idempotent, so calling it more than
        once per change costs a traversal and nothing else.
        """
        height = 0
        for node in self:
            height += node.block_height
        self.height = height

        for node in self:
            self.update_node(node, coord)

        grid = self.grid
        if grid is not None:
            grid.mark_dirty()

    def update_node(self, node: GameNode, coord: Coord) -> None:
        """Position and register one direct member of the cell."""
        t = self.get_block_transform(node, coord)
        node.position = glm.vec2(t.x, t.y)
        self._attach(node, coord)

        for member in self._members_of(node):
            self.update_member(node, member, coord)

    def update_member(self, group: GameNode, member: GameNode, coord: Coord) -> None:
        """Position and register a node nested inside a group.

        Being inside a group does not exempt a node from being a grid child:
        it still needs a coord, a grid reference and a position.
        """
        base = Transform(group.position.x, group.position.y)
        vu = group.vu
        if vu is not None and hasattr(vu, "get_member_transform"):
            t = vu.get_member_transform(base, member)
            member.position = glm.vec2(t.x, t.y)
        else:
            member.position = glm.vec2(group.position)

        self._attach(member, coord)

    # ------------------------------------------------------------------
    # Build / clone
    # ------------------------------------------------------------------

    def build(self, app, coord: Coord) -> None:
        if self.ctors:
            execute_ctors(app, self.ctors, coord, self)

    def clone(self, row: "Row" = None) -> "Cell":
        clone = Cell(row)
        clone.ctors = self.ctors
        return clone

    # ------------------------------------------------------------------
    # Mutation -- these only change the list, then call update
    # ------------------------------------------------------------------

    def find_group(self):
        for node in self:
            if isinstance(node, GroupBlock):
                return node
        return None

    def push_node(self, node: GameNode, coord: Coord) -> None:
        """Add a node to the top of the stack.

        Single exit. Every branch decides only *where in the structure* the
        node goes; `update` then positions and registers whatever is present,
        so no branch can leave a node unregistered. The previous version
        branched three ways and only one branch registered, which is why a
        block pushed onto an existing group never got a coord or a position.
        """

        if len(self) == 0:
            self.append(node)
        elif node.groupable:
            top = self[-1]
            group = self.find_group()
            if group is not None:
                group.push_node(node)
            elif top.groupable:
                # Absorb the current top into a new group.
                old_top = self.pop()
                group = GroupBlock()
                group.push_node(old_top)
                group.push_node(node)
                self.append(group)
            else:
                self.append(node)
        else:
            self.append(node)

        self.update(coord)

    def pop_node(self, coord: Coord = None):
        if len(self) == 0:
            return None
        node = self[-1]
        self.remove_node(node, coord if coord is not None else node.coord)
        return node

    def remove_node(self, node: GameNode, coord: Coord = None) -> None:
        """Remove a node, collapsing any group it leaves empty or redundant.

        Group members are not in `self`, so membership is resolved before the
        `node in self` test. The original recursed through
        `self.remove_node(group)`, which re-entered the group branch and found
        the same group again whenever GroupBlock.groupable is True.
        """
        coord = coord if coord is not None else node.coord

        group = self.find_group()
        if group is not None and node is not group and node in self._members_of(group):
            group.remove_node(node)
            self._detach(node)

            if group.empty():
                self._unlink(group)
            elif group.redundant():
                # ASSUMPTION: nodes[0] is the sole survivor, as originally.
                member = group.nodes[0]
                group.remove_node(member)
                self._unlink(group)
                self.push_node(member, coord)
                return

            self.update(coord)
            return

        if node not in self:
            logger.warning(f"Node not found in cell: {node}")
            return

        self._unlink(node)
        self.update(coord)

    def _unlink(self, node: GameNode) -> None:
        """Remove a direct member without repositioning.

        Callers batch the `update` so a group collapse repositions the stack
        once instead of three times.
        """
        list.remove(self, node)
        self._detach(node)

    def clear_nodes(self) -> None:
        for node in list(self):
            self._detach(node)
        list.clear(self)
        self.height = 0

        grid = self.grid
        if grid is not None:
            grid.mark_dirty()

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get_top(self):
        return self[-1] if len(self) else None

    def get_top_block(self):
        for top in reversed(self):
            if isinstance(top, (GroupBlock, Block)):
                return top
        return None

    # ------------------------------------------------------------------
    # Transforms
    # ------------------------------------------------------------------

    def get_top_transform(self, coord: Coord):
        """Transform at the top of the stack."""
        t = Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT)
        t.y += self.height * BLOCK_STACK_HEIGHT
        return t

    def get_bottom_transform(self, coord: Coord):
        """Transform at the bottom of the stack."""
        return Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT)

    def get_node_transform(self, target_node, coord: Coord):
        """Transform of any node, including one nested in a group."""
        if isinstance(target_node, Block):
            return self.get_block_transform(target_node, coord)

        blit_up = 0
        for node in self:
            blit_up += node.block_height * BLOCK_STACK_HEIGHT
            if isinstance(node, GroupBlock):
                return node.get_member_transform(
                    Transform(
                        coord.x * BLOCK_WIDTH,
                        coord.y * BLOCK_ROW_HEIGHT + blit_up,
                    ),
                    target_node,
                )

        return Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT + blit_up)

    def get_block_transform(self, block, coord: Coord):
        """Transform of a direct member of this cell.

        This sums `block_height` for every node below `block`, with no vu
        check. The original skipped vu-less nodes here but counted them in the
        cell's height total, so a vu-less node raised the stack height without
        raising the blocks above it. Restore `if node.vu is not None` if that
        asymmetry was deliberate.
        """
        blit_up = 0
        for node in self:
            if node is block:
                break
            blit_up += node.block_height * BLOCK_STACK_HEIGHT

        return Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT + blit_up)
