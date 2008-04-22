from block import *

'''
This is an interesting solution.  Too bad I don't want to use it. :(
http://mail.python.org/pipermail/python-list/2008-February/476992.html
...
class RDFObject(object):
    _cache = {}   # class variable is shared among all RDFObject
instances
    class __metaclass__(type):
        def __call__(cls, *args, **kwargs):
            return cls.__new__(cls, *args, **kwargs)
    def __new__(cls, uri, *args, **kargs):
        if uri not in cls._cache:
            obj = object.__new__(cls)
            cls._cache[uri] = obj
            obj.__init__(uri, *args, **kargs)
        return cls._cache[uri]
    def __init__(self, uri):
        self.uri = uri
        print self.__class__, uri
'''
'''
http://mail.python.org/pipermail/python-list/2008-February/477029.html
...
    def __new__(cls, uri, *args, **kwargs):
        obj = cls._cache.get(uri, None):
        if obj is None:
            obj = cls._cache[uri] = object.__new__(cls)
            obj.__init__(uri, *args, **kwargs)
        return obj
'''

'''
BuildingBlock
'''
BuildingBlock_cache = {}

class BuildingBlock(Block):
    def __new__(cls, item, *args, **kargs):
        global BuildingBlock_cache
        uri = item.name
        if uri not in BuildingBlock_cache:
            obj = object.__new__(cls)
            BuildingBlock_cache[uri] = obj
            obj.__init__(item, *args, **kargs)
        else:
            obj = BuildingBlock_cache[uri]
        return obj
        
    def __init__(self, item):
        super(BuildingBlock, self).__init__()
        self.vu = BlockVu(self, item.imgSrc)
        self.vacancy = False