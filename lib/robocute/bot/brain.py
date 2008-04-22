import robocute.entity
from robocute.base import Coord

class Brain(robocute.entity.Brain):

    def __init__(self, node):
        super(Brain, self).__init__(node)

    def can_transfer(self, node, srcCoord, dstCoord):
        #boundary check
        if(not self.grid.valid_coord(dstCoord)):
            return False
        #destination check
        top = self.grid.get_top_block_at(dstCoord)
        if not top or not top.vacancy:
           return False
       #good to go
        return True
    
    def transfer_to(self, dstCoord):
        self.transfer(self.node, self.coord, dstCoord)
        
    def transfer(self, node, srcCoord, dstCoord):
       if(not self.can_transfer(node, srcCoord, dstCoord)):
           return False
       #else
       srcCell = self.grid.get_cell_at(srcCoord)
       srcCell.remove_node(node)
       #
       dstCell = self.grid.get_cell_at(dstCoord)
       dstCell.push_node(node)
       #
       _dstCoord = Coord(dstCoord.x, dstCoord.y, dstCell.height)
       #self.set_coord(dstCoord)
       self.coord = _dstCoord
