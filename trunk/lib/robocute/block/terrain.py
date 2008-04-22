from block import *

'''
BrownBlock
'''
BrownBlock_singleton = None

class BrownBlock(Block):
    def __new__(cls, *args, **kargs):
        global BrownBlock_singleton
        if not BrownBlock_singleton:
            obj = object.__new__(cls)
            BrownBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return BrownBlock_singleton
        
    def __init__(self):
        super(BrownBlock, self).__init__()
        self.vu = BlockVu(self, 'Brown Block.png')
        self.vacancy = True

'''
PlainBlock
'''
PlainBlock_singleton = None

class PlainBlock(Block):
    def __new__(cls, *args, **kargs):
        global PlainBlock_singleton
        if not PlainBlock_singleton:
            obj = object.__new__(cls)
            PlainBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return PlainBlock_singleton
        
    def __init__(self):
        super(PlainBlock, self).__init__()
        self.vu = BlockVu(self, 'Plain Block.png')
        self.vacancy = True

'''
RampNorth
'''
RampNorth_singleton = None

class RampNorth(Block):
    def __new__(cls, *args, **kargs):
        global RampNorth_singleton
        if not RampNorth_singleton:
            obj = object.__new__(cls)
            RampNorth_singleton = obj
            obj.__init__(*args, **kargs)
        return RampNorth_singleton
        
    def __init__(self):
        super(RampNorth, self).__init__()
        self.vu = BlockVu(self, 'Ramp North.png')
        self.vacancy = True

'''
RampSouth
'''
RampSouth_singleton = None

class RampSouth(Block):
    def __new__(cls, *args, **kargs):
        global RampSouth_singleton
        if not RampSouth_singleton:
            obj = object.__new__(cls)
            RampSouth_singleton = obj
            obj.__init__(*args, **kargs)
        return RampSouth_singleton
        
    def __init__(self):
        super(RampSouth, self).__init__()
        self.vu = BlockVu(self, 'Ramp South.png')
        self.vacancy = True

'''
WallBlockTall
'''
WallBlockTall_singleton = None

class WallBlockTall(Block):
    def __new__(cls, *args, **kargs):
        global WallBlockTall_singleton
        if not WallBlockTall_singleton:
            obj = object.__new__(cls)
            WallBlockTall_singleton = obj
            obj.__init__(*args, **kargs)
        return WallBlockTall_singleton
        
    def __init__(self):
        super(WallBlockTall, self).__init__()
        self.vu = BlockVu(self, 'Wall Block Tall.png')
        self.vacancy = True

'''
WallBlock
'''
WallBlock_singleton = None

class WallBlock(Block):
    def __new__(cls, *args, **kargs):
        global WallBlock_singleton
        if not WallBlock_singleton:
            obj = object.__new__(cls)
            WallBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return WallBlock_singleton
        
    def __init__(self):
        super(WallBlock, self).__init__()
        self.vu = BlockVu(self, 'Wall Block.png')
        self.vacancy = True

'''
WoodBlock
'''
WoodBlock_singleton = None

class WoodBlock(Block):
    def __new__(cls, *args, **kargs):
        global WoodBlock_singleton
        if not WoodBlock_singleton:
            obj = object.__new__(cls)
            WoodBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return WoodBlock_singleton
        
    def __init__(self):
        super(WoodBlock, self).__init__()
        self.vu = BlockVu(self, 'Wood Block.png')
        self.vacancy = True

'''
DirtBlock
'''
DirtBlock_singleton = None

class DirtBlock(Block):
    def __new__(cls, *args, **kargs):
        global DirtBlock_singleton
        if not DirtBlock_singleton:
            obj = object.__new__(cls)
            DirtBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return DirtBlock_singleton
        
    def __init__(self):
        super(DirtBlock, self).__init__()
        self.vu = BlockVu(self, 'Dirt Block.png')
        self.vacancy = True
        
StoneBlock_singleton = None

class StoneBlock(Block):
    def __new__(cls, *args, **kargs):
        global StoneBlock_singleton
        if not StoneBlock_singleton:
            obj = object.__new__(cls)
            StoneBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return StoneBlock_singleton
    
    def __init__(self):
        super(StoneBlock, self).__init__()
        self.vu = BlockVu(self, 'Stone Block.png')
        self.vacancy = True

StoneBlockTall_singleton = None

class StoneBlockTall(Block):
    def __new__(cls, *args, **kargs):
        global StoneBlockTall_singleton
        if not StoneBlockTall_singleton:
            obj = object.__new__(cls)
            StoneBlockTall_singleton = obj
            obj.__init__(*args, **kargs)
        return StoneBlockTall_singleton
    
    def __init__(self):
        super(StoneBlockTall, self).__init__()
        self.vu = BlockVu(self, 'Stone Block Tall.png')
        self.height = 2
        self.vacancy = True

RampWest_singleton = None

class RampWest(Block):
    def __new__(cls, *args, **kargs):
        global RampWest_singleton
        if not RampWest_singleton:
            obj = object.__new__(cls)
            RampWest_singleton = obj
            obj.__init__(*args, **kargs)
        return RampWest_singleton
    
    def __init__(self):
        super(RampWest, self).__init__()
        self.vu = BlockVu(self, 'Ramp West.png')
        self.vacancy = True

RampEast_singleton = None

class RampEast(Block):
    def __new__(cls, *args, **kargs):
        global RampEast_singleton
        if not RampEast_singleton:
            obj = object.__new__(cls)
            RampEast_singleton = obj
            obj.__init__(*args, **kargs)
        return RampEast_singleton
    
    def __init__(self):
        super(RampEast, self).__init__()
        self.vu = BlockVu(self, 'Ramp East.png')
        self.vacancy = True

GrassBlock_singleton = None
    
class GrassBlock(Block):
    def __new__(cls, *args, **kargs):
        global GrassBlock_singleton
        if not GrassBlock_singleton:
            obj = object.__new__(cls)
            GrassBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return GrassBlock_singleton
    
    def __init__(self):
        super(GrassBlock, self).__init__()
        self.vu = BlockVu(self, 'Grass Block.png')


WaterBlock_singleton = None

class WaterBlock(Block):
    def __new__(cls, *args, **kargs):
        global WaterBlock_singleton
        if not WaterBlock_singleton:
            obj = object.__new__(cls)
            WaterBlock_singleton = obj
            obj.__init__(*args, **kargs)
        return WaterBlock_singleton
    def __init__(self):
        super(WaterBlock, self).__init__()
        self.vu = BlockVu(self, 'Water Block.png')
