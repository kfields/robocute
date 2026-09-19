from robocute.block import *

'''
BuildingBlock
'''
class BuildingBlock(Block):
    _cache = {}    
    def __new__(cls, dna, *args, **kargs):
        uri = dna.name
        if uri not in cls._cache:
            obj = object.__new__(cls)
            obj.dna = dna
            cls._cache[uri] = obj
            obj.__init__(dna, *args, **kargs)
        else:
            obj = cls._cache[uri]
        return obj
        
    def __init__(self, dna):
        super().__init__(dna)
        self.add_chip(BlockVu(self.dna.img_src))
        self.vacancy = False