import robocute.brain

class Brain(robocute.brain.Brain):

    def __init__(self, node):
        super(Brain, self).__init__(node)

    def can_transfer(self, node, srcCoord, dstCoord):
        #boundary check
        if(not self.scene.valid_coord(dstCoord)):
            return False
        #destination check
        top = self.scene.get_top_block_at(dstCoord)
        if(not top.has_vacancy()):
           return False
       #good to go
        return True
    
    def transfer_to(self, dstCoord):
        self.transfer(self.node, self.coord, dstCoord)
        
    def transfer(self, node, srcCoord, dstCoord):
       if(not self.can_transfer(node, srcCoord, dstCoord)):
           return False
       #else
       srcCell = self.scene.get_cell_at(srcCoord)
       srcCell.remove_node(node)
       #
       dstCell = self.scene.get_cell_at(dstCoord)
       dstCell.push_node(node)
       #
       self.set_coord(dstCoord)
