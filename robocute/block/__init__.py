from loguru import logger

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.scheduler import Scheduler

from robocute.entity import *
from robocute.vu import *
from robocute.builder import find_dna, add_class, add_classes

sprite_loader = SpriteLoader()

SPAWN_DELAY = 3.0


class BlockVu(SpriteVu):
    def __init__(self, img_src):
        path = ResourceManager().resolve_path("${resources}/image/" + img_src)
        sprite = sprite_loader.load(path)
        super().__init__(sprite)

    def validate(self):
        super().validate()
        self.hotHeight = self.node.height * BLOCK_HOT_HEIGHT


class Block(Entity):
    groupable = False

    def __init__(self, dna):
        super().__init__(dna)


class GroupBlock(Block):
    """
    A block that stacks member nodes in `self.nodes`.

    Members are NOT node children: this block draws them through
    `yield_visuals`, and nothing here calls their `update`. Whoever owns the
    members (their brains, the scene) is responsible for updating them.
    """

    def __init__(self, dna=None):
        if not dna:
            dna = find_dna("GroupBlock")
        super().__init__(dna)
        self.nodes = []
        self.vacancy = True
        self.dirty = True

    def _recompute_height(self):
        self.block_height = max((node.block_height for node in self.nodes), default=0)

    def update(self, delta_time: float):
        # Cheap, and catches members whose block_height changes after joining.
        self._recompute_height()
        super().update(delta_time)

    def push_node(self, node):
        self.nodes.append(node)
        # Was self.update(0.), which ran a full node update (and everything
        # it cascades to) on every push just to recompute the height.
        self._recompute_height()
        self.dirty = True

    def remove_node(self, node):
        self.nodes.remove(node)
        self._recompute_height()
        self.dirty = True

    def empty(self):
        return len(self.nodes) == 0

    def redundant(self):
        return len(self.nodes) == 1

    def get_member_transform(self, transform, member):
        t = transform.copy()
        for node in self.nodes:
            t.x += 10
            t.y -= 10
            if node is member:
                break
        t.y += member.height * BLOCK_STACK_HEIGHT
        return t

    def yield_visuals(self):
        """Yield the group's own visual, then its members', bottom to top."""
        yield from super().yield_visuals()
        for node in self.nodes:
            yield from node.yield_visuals()


class HomeBlock(GroupBlock):
    def register(self, app, coord):
        app.add_home(self, coord)


class SpawnBlock(GroupBlock):
    """Holds a spawn node; when it's taken, a fresh copy reappears once the block is empty."""

    def __init__(self, spawn):
        super().__init__()
        self.spawn = spawn
        self._respawn_task = None
        if spawn is not None:
            self.push_node(spawn)

    def schedule_respawn(self, delay=SPAWN_DELAY):
        # Was pyglet's `clock`, which no longer exists here (NameError).
        if self._respawn_task is not None:
            self._respawn_task.cancel()
        self._respawn_task = Scheduler().schedule_once(lambda _elapsed: self.respawn(), delay)

    def remove_node(self, node):
        super().remove_node(node)
        if node is self.spawn:
            self.spawn = self.spawn.copy()
            self.schedule_respawn()

    def respawn(self):
        self._respawn_task = None
        if self.empty():
            # Was add_node(), which adds a node child rather than a group member.
            self.push_node(self.spawn)
        else:
            self.schedule_respawn()

    def delete(self):
        if self._respawn_task is not None:
            self._respawn_task.cancel()
            self._respawn_task = None
        super().delete()


add_class(SpawnBlock)