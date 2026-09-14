from robocute.block import *

'''
TerrainBlock
'''
class TerrainBlock(Block):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vacancy = True
        self.add(BlockVu(self.dna.imgSrc))
    '''
    def _seat(self):
        super()._seat()
        self.add(BlockVu(self.dna.imgSrc))
    '''