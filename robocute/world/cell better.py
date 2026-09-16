from typing import TYPE_CHECKING

from loguru import logger
import glm

from robocute.base import *
from robocute.block import *
from robocute.builder import execute_ctors
from robocute.node import GameNode

if TYPE_CHECKING:
    from .row import Row


class Cell(list):
    def __init__(self, row: "Row" = None):
        super().__init__()
        self.row = row
        self.invalid = 0
        self.height = 0
        self.ctors = None

    """
    def __getstate__(self):
        return self.__dict__
                
    def __setstate__(self, state):
        self.__dict__ = state
    """

    @property
    def grid(self):
        return self.row.grid if self.row else None

    def invalidate(self, flag=1):
        if self.invalid == 0:
            self.row.invalidate()
        self.invalid |= flag

    def validate(self):
        self.invalid = 0

    def update(self, coord: Coord):
        height = 0
        for node in self:
            height += node.block_height
            self.update_node(node, coord)
        self.height = height

        self.grid.mark_dirty()

    def update_node(self, node: GameNode, coord: Coord):
        logger.debug(f"Adding node: {node} at coord: {coord}")
        t = self.get_block_transform(node, coord)
        node.coord = coord
        node.grid = self.grid
        node.position = glm.vec2(t.x, t.y)
        """
        if node.position.y > 1028:
            raise ValueError(f"Node position y exceeds limit: {node.position.y}")
        """
        # logger.debug("Coord.x: {}", coord.x)
        # logger.debug("Coord.y: {}", coord.y)
        # logger.debug("Node position set to: {}", node.position)

        if node.parent is None and not self.grid.is_template:
            self.grid.add_child(node)

    '''
    def update(self):
        height = 0
        for node in self:
            height += node.block_height
        self.height = height
        self.grid.mark_dirty()
    '''

    def build(self, app, row, coord):
        self.row = row
        if self.ctors:
            execute_ctors(app, self.ctors, coord, self)

    def clone(self):
        clone = Cell()
        clone.ctors = self.ctors
        return clone

    def find_group(self):
        for node in self:
            if isinstance(node, GroupBlock):
                return node
        return None

    def push_node(self, node, coord: Coord):
        self.invalidate()
        if len(self) ==0:
            self.append(node)
            self.update(coord)
            return
        #else
        top = self[-1]
        if node.groupable:
            group = self.find_group()        
            if group:
                group.push_node(node)
            elif top.groupable:
                oldTop = self.pop()
                top = GroupBlock()
                top.push_node(oldTop)
                top.push_node(node)
                self.append(top)
            else:
                self.append(node)
        else:
            self.append(node)
        self.update(coord)

    '''
    def push_node(self, node: GameNode, coord: Coord):
        logger.debug(f"Pushing node: {node.__class__.__name__} at coord: {coord}")
        #self.invalidate()
        if len(self) == 0:
            self.add_node(node, coord)
            return
        # else
        top = self[-1]

        if node.groupable:
            group = self.find_group()
            if group:
                logger.debug(f"Found group: {group}")
                group.push_node(node)
                #self.update_node(node, coord)
            elif top.groupable:
                logger.debug(f"Top node is groupable: {top.groupable}")
                oldTop = self.pop()
                top = GroupBlock()
                top.push_node(oldTop)
                top.push_node(node)
                self.append(top)
                self.update_node(top, coord)
            else:
                logger.debug(f"Top node is not groupable: {top.groupable}")
                self.append(node)
                self.update_node(node, coord)
        else:
            self.add_node(node, coord)

        self.update()

    def add_node(self, node: GameNode, coord: Coord):
        self.update()
        self.append(node)
        self.update_node(node, coord)
        #self.append(node)
        #self.update()

    def update_node(self, node: GameNode, coord: Coord):
        logger.debug(f"Adding node: {node} at coord: {coord}")
        t = self.get_node_transform(node, coord)
        node.coord = coord
        node.grid = self.grid
        node.position = glm.vec2(t.x, t.y)
        """
        if node.position.y > 1028:
            raise ValueError(f"Node position y exceeds limit: {node.position.y}")
        """
        # logger.debug("Coord.x: {}", coord.x)
        # logger.debug("Coord.y: {}", coord.y)
        # logger.debug("Node position set to: {}", node.position)

        if node.parent is None and not self.grid.is_template:
            self.grid.add_child(node)
    '''

    def pop_node(self):
        exit()
        node = self[-1]
        self.remove(node)
        self.update()
        return node

    def remove_node(self, node: GameNode):
        logger.debug(f"Removing node: {node}")
        logger.debug(f"Cell before removing node: {self}")
        if not node in self:
            return
        #self.invalidate()
        if node.groupable:
            group = self.find_group()
            if group:
                group.remove_node(node)
                if group.empty():
                    self.remove_node(group)  # watchme:recursive
                elif group.redundant():
                    member = group.nodes[0]
                    self.remove_node(group)  # watchme:recursive
                    self.push_node(member)
                self.update()
                return
        # else
        self.remove(node)
        self.update(node.coord)

    def get_top(self):
        length = len(self)
        if length == 0:
            return None
        top = self[-1]
        return top

    def get_top_block(self):
        length = len(self)
        if length == 0:
            return None
        for top in reversed(self):
            if isinstance(
                top, GroupBlock
            ):  # cripes!  It is shallow testing! Good in a way.
                break
            if isinstance(top, Block):
                break
        return top

    """
    Get transform at top of cell
    """

    def get_top_transform(self, coord):
        t = Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT)
        t.y += self.height * BLOCK_STACK_HEIGHT
        return t

    """
    Get transform at bottom of cell
    """

    def get_bottom_transform(self, coord):
        t = Transform(coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT)
        return t

    """
    Get transform of node at coordinate
    """

    def get_node_transform(self, targetNode, coord):
        if isinstance(targetNode, Block):
            return self.get_block_transform(targetNode, coord)
        # else
        blitUp = 0
        for node in self:
            vu = node.vu
            blitUp = blitUp + node.block_height * BLOCK_STACK_HEIGHT
            if isinstance(node, GroupBlock):
                return vu.get_member_transform(
                    Transform(
                        coord.x * BLOCK_WIDTH, coord.y * BLOCK_ROW_HEIGHT + blitUp
                    ),
                    targetNode,
                )
        blitY = coord.y * BLOCK_ROW_HEIGHT
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t


    """
    This will get the transform of any block.
    """

    def get_block_transform(self, block, coord):
        blitUp = 0
        for node in self:
            if node == block:
                break
            vu = node.vu
            if vu != None:
                blitUp = blitUp + node.block_height * BLOCK_STACK_HEIGHT
        blitY = coord.y * BLOCK_ROW_HEIGHT
        t = Transform(coord.x * BLOCK_WIDTH, blitY + blitUp)
        return t
