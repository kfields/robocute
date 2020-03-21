import copy

'''
This file is the bottom of the import heirarchy so I'm gonna stick fundamentals in here for now.
'''

'''
BLOCK_WIDTH = 101
BLOCK_HEIGHT = 171
BLOCK_STACK_HEIGHT = 40
BLOCK_ROW_HEIGHT = 85
BLOCK_HOT_HEIGHT = 120
'''
BLOCK_WIDTH = 101
BLOCK_HEIGHT = 171
BLOCK_STACK_HEIGHT = 40
BLOCK_ROW_HEIGHT = 85
BLOCK_HOT_HEIGHT = BLOCK_ROW_HEIGHT + BLOCK_STACK_HEIGHT 
#
INV_BLOCK_WIDTH = 1. / BLOCK_WIDTH
INV_BLOCK_HEIGHT = 1. / BLOCK_HEIGHT
INV_BLOCK_STACK_HEIGHT = 1. / BLOCK_STACK_HEIGHT
INV_BLOCK_ROW_HEIGHT = 1. / BLOCK_ROW_HEIGHT
#
WORLD_GRID_ROW_MAX = 64
WORLD_GRID_COL_MAX = 64
WORLD_GRID_CACHE_ROW_COUNT= 64
WORLD_GRID_CACHE_COL_COUNT = 64
#
WORLD_GRID_WIDTH = WORLD_GRID_COL_MAX * BLOCK_WIDTH
WORLD_GRID_HEIGHT = WORLD_GRID_ROW_MAX * BLOCK_ROW_HEIGHT
WORLD_GRID_CACHE_WIDTH = WORLD_GRID_CACHE_COL_COUNT * WORLD_GRID_WIDTH
WORLD_GRID_CACHE_HEIGHT = WORLD_GRID_CACHE_ROW_COUNT * WORLD_GRID_HEIGHT
#
INV_WORLD_GRID_WIDTH = 1. / WORLD_GRID_WIDTH
INV_WORLD_GRID_HEIGHT = 1. / WORLD_GRID_HEIGHT
INV_WORLD_GRID_CACHE_WIDTH = 1. / WORLD_GRID_CACHE_WIDTH
INV_WORLD_GRID_CACHE_HEIGHT = 1. / WORLD_GRID_CACHE_HEIGHT

'''
Block Coordinates
'''
class Coord:
    def __init__(self, cellX, cellY, cellZ = 0):
        self.x = cellX
        self.y = cellY
        self.z = cellZ

    def to_transform(self):
        t = Transform(self.x * BLOCK_WIDTH, self.y * BLOCK_ROW_HEIGHT)
        t.y += self.z * BLOCK_STACK_HEIGHT
        return t
        
'''
2D position and rotation
'''
class Transform:
    def __init__(self, x, y, r=0):
        self.x = x
        self.y = y
        self.r = r
        
    def copy(self):
        return copy.copy(self)
'''
'''
class Base(object):
    def __init__(self, dna = None):
        self.invalid = 0
        self.dna = dna

    def delete(self):
        pass
    
    def register(self, app, coord = None):
        #pass
        self.validate()
        
    def invalidate(self, flag = 1):
        self.invalid |= flag
        #print 'invalid'
        
    def validate(self):
        self.invalid = 0

    def copy(self):
        return copy.copy(self)
    
    def deep_copy(self):
        return copy.deepcopy(self)
'''
'''
