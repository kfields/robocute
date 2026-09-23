from . import globe

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.resource.resource_manager import ResourceManager

from robocute.brain import BaseBrain
from robocute.node import GameNode
from robocute.base import Coord


ENTITY_HOT_HEIGHT = 120


class EntityVu(SpriteVu):
    def __init__(self, img_src):
        path = ResourceManager().resolve_path("${resources}/image/" + img_src)
        sprite = SpriteLoader().load(path)
        super().__init__(sprite)
        self.hotHeight = ENTITY_HOT_HEIGHT


class Entity(GameNode):
    groupable = True

    def __init__(self, dna=None, fn=None):
        super().__init__(dna, fn)
        self.block_height = 1
        self.vacancy = True
        self.grid = None
        self.construct_vu()

    def construct_vu(self):
        if self.dna.img_src:
            self.vu = self.add_chip(EntityVu(self.dna.img_src))


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
