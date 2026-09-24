from robocute.brain import BaseBrain

class EntityBrain(BaseBrain):
    """
    Position lives on the node: `coord` and `old_coord` are read-only views of
    `node.coord` / `node.old_coord`. Movement code must update the node, not the brain.
    """

    def __init__(self):
        super().__init__()
        self.on_move = None  # Camera callback, fired after the entity moves

    @property
    def coord(self):
        return self.node.coord if self.node is not None else None

    @property
    def old_coord(self):
        return self.node.old_coord if self.node is not None else None

    def register(self, app, coord):
        # Was `self.app.world...` (ignoring the `app` argument) followed by
        # `self.coord = coord`, which raises AttributeError: coord has no setter.
        self.grid = app.world.get_grid_at(coord)
