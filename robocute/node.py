from crunge.engine.d2 import Node2D

from .base import Transform, Coord


class GameNode(Node2D):
    def __init__(self, dna=None, fn=None):
        super().__init__()
        self.dna = dna
        self.fn = fn  # not sure about this...

        self.name = "Unknown"
        self.brain = None
        self.coord: Coord = None

    def register(self, app, coord=None):
        # pass
        self.coord = coord
        self.validate()

    def invalidate(self, flag=1):
        pass

    def validate(self):
        pass

    # events
    def process(self, event):
        if self.fn:
            self.fn(self)

    def set_transform(self, transform):
        raise NotImplementedError(
            "set_transform method must be implemented by subclass"
        )
        self.x = transform.x
        self.y = transform.y

    def get_transform(self):
        return Transform(self.x, self.y)
