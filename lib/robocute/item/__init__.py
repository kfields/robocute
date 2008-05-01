
from robocute.entity import *
from robocute.sprite import *
   
class Item(Entity):
    def __init__(self):
        super(Item, self).__init__()

'''
Treasure
'''
class Treasure(Item):
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
        super(Treasure, self).__init__()
        self.worth = 0
        self.name = item.title
        self.vu = SpriteVu(self, item.imgSrc)

'''
Special
'''
class Special(Item):
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
        super(Special, self).__init__()
        self.name = item.title
        self.vu = SpriteVu(self, item.imgSrc)
