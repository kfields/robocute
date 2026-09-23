from crunge.engine.d2 import Node2D

from .base import Transform, Coord


class GameNode(Node2D):
    def __init__(self, dna=None, fn=None):
        super().__init__()
        self.dna = dna
        self.fn = fn  # not sure about this...

        self.name = "Unknown"
        self.brain = None
        self._coord: Coord = None
        self._old_coord: Coord = None

    @property
    def coord(self):
        return self._coord

    @coord.setter
    def coord(self, value):
        self._coord = value
        #self._old_coord = self._coord

    @property
    def old_coord(self):
        return self._old_coord

    @old_coord.setter
    def old_coord(self, value):
        self._old_coord = value

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

    def yield_visuals(self):
        """Yield this node's visuals in draw order.

        A plain node contributes its own vu, if it has one. Container nodes
        override this to yield what they hold instead.
        """
        vu = self.vu
        if vu is not None:
            yield vu