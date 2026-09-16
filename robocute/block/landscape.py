from robocute.block import *

'''
LandscapeBlock
'''
class LandscapeBlock(Block):
    def __init__(self, dna):
        super().__init__(dna)
        self.vacancy = False

    def construct_vu(self):
        self.vu = self.add(BlockVu(self.dna.img_src))
