from robocute.entity import EntityBrain
from robocute.base import Coord


class BotBrain(EntityBrain):
    def can_transfer(self, node, src_coord, dst_coord):
        if not self.grid.valid_coord(dst_coord):
            return False
        top = self.grid.get_top_block_at(dst_coord)
        if not top or not top.vacancy:
            return False
        return True

    def transfer_to(self, dst_coord):
        return self.transfer(self.node, self.coord, dst_coord)

    def transfer(self, node, src_coord, dst_coord):
        """Move `node` from `src_coord` to `dst_coord`. Returns True if it moved."""
        if not self.can_transfer(node, src_coord, dst_coord):
            return False

        src_cell = self.grid.get_cell_at(src_coord)
        src_cell.remove_node(node)

        dst_cell = self.grid.get_cell_at(dst_coord)
        dst_cell.push_node(node, dst_coord)

        # In the pyglet version this was `self.coord = ...`. Position now lives
        # on the node, and with that line commented out nothing updated it,
        # so the brain kept pathing from its starting cell every step.
        node.old_coord = src_coord
        node.coord = Coord(dst_coord.x, dst_coord.y, dst_cell.height)
        return True
