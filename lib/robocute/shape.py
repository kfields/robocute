
import copy

class Shape(object):
    def __init__(self):
        super(Shape, self).__init__()

    def copy(self):
        return copy.copy(self)

    def deep_copy(self):
        return copy.deepcopy(self)

class Rect(Shape):
    def __init__(self, x = 0, y = 0, z = 1., width = 0, height = 0):
        super(Rect, self).__init__()
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height