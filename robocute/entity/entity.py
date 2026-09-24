from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.resource.resource_manager import ResourceManager

from ..node import GameNode


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
