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
            obj.__init__(*args, **kargs)
        else:
            obj = cls._cache[uri]
        return obj
        
    def __init__(self):
        super(BuildingBlock, self).__init__()
        self.vu = BlockVu(self, self.dna.imgSrc)
        self.vacancy = False