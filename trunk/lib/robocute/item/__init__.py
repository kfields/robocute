
from robocute.entity import *
from robocute.sprite import *
   
class Item(Entity):
    def __init__(self, dna):
        super(Item, self).__init__(dna)

'''
Treasure
'''
class Treasure(Item):
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
        
    def __init__(self, dna):
        super(Treasure, self).__init__(dna)
        self.worth = 0
        self.name = dna.title
        self.vu = SpriteVu(self, dna.imgSrc)

'''
Special
'''
class Special(Item):
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
        
    def __init__(self, dna):
        super(Special, self).__init__(dna)
        self.name = dna.title
        self.vu = SpriteVu(self, dna.imgSrc)
