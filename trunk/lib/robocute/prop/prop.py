import data

from robocute.block.block import Block, BlockVu
from robocute.vu import *


class Prop(Block):
    def __init__(self):
        super(Prop, self).__init__()

class TreeShort(Prop):
    singleton = None
    def factory(cls, *args):
        if(cls.singleton == None):
            cls.singleton = TreeShort()
        return cls.singleton
    
    def __init__(self):
        super(TreeShort, self).__init__()
        self.vu = BlockVu(self, 'Tree Short.png')
