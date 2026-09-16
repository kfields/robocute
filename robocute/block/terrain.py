from robocute.block import *

'''
TerrainBlock
'''
class TerrainBlock(Block):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vacancy = True
        self.add(BlockVu(self.dna.img_src))
    '''
    def _seat(self):
        super()._seat()
        self.add(BlockVu(self.dna.img_src))
    '''