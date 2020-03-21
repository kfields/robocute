from robocute.block import *

'''
TerrainBlock
'''
class TerrainBlock(Block):
    _cache = {}    
    def __new__(cls, dna, *args, **kargs):
        uri = dna.name
        if uri not in cls._cache:
            obj = object.__new__(cls)
            cls._cache[uri] = obj
            obj.__init__(dna, *args, **kargs)
        else:
            obj = cls._cache[uri]
        return obj
        
    def __init__(self, dna = None):
        super().__init__(dna)
        self.vu = BlockVu(self, self.dna.imgSrc)
        self.vacancy = True