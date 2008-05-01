from robocute.block import *

'''
BuildingBlock
'''
class BuildingBlock(Block):
    _cache = {}    
    def __new__(cls, item, *args, **kargs):
        uri = item.name
        if uri not in cls._cache:
            obj = object.__new__(cls)
            cls._cache[uri] = obj
            obj.__init__(item, *args, **kargs)
        else:
            obj = cls._cache[uri]
        return obj
        
    def __init__(self, item):
        super(BuildingBlock, self).__init__()
        self.vu = BlockVu(self, item.imgSrc)
        self.vacancy = False