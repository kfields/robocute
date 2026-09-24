from loguru import logger
import glm

from crunge import sdl

from robocute.widget.bubble import *

from robocute.message import *
from robocute.robo.message import *

from ..bot import BotBrain
from ..base import Coord

from .speech_bubble import SpeechBubble


BUBBLE_OFFSET_Y = 32

# (dx, dy) for each directional message
_GO_OFFSETS = {
    GoNorth: (0, 1),
    GoEast: (1, 0),
    GoSouth: (0, -1),
    GoWest: (-1, 0),
}

_KEY_MESSAGES = {
    sdl.SDLK_w: GoNorth,
    sdl.SDLK_s: GoSouth,
    sdl.SDLK_a: GoWest,
    sdl.SDLK_d: GoEast,
}


class RoboBrain(BotBrain):
    def __init__(self):
        super().__init__()
        self.bubble = None

    def delete(self):
        self.del_bubble()
        super().delete()

    # ---------------------------------------------------------------- bubbles

    def say(self, items):
        self.del_bubble()
        self.bubble = SpeechBubble(items)
        self.add_bubble(self.bubble)

    def add_bubble(self, bubble):
        # Lower-left corner pinned beside the head; the bubble re-pins it
        # after each layout pass, so it grows up and to the right.
        bubble.anchor = self.node.position + glm.vec2(self.node.width / 2, BUBBLE_OFFSET_Y)
        self.app.scene.add_bubble(bubble)

    def del_bubble(self):
        if self.bubble is not None:
            self.app.scene.remove_bubble(self.bubble)
            self.bubble = None

    # --------------------------------------------------------------- movement

    def go(self, msg):
        offset = next(
            (off for cls, off in _GO_OFFSETS.items() if isinstance(msg, cls)), None
        )
        if offset is None:
            logger.warning(f"Unknown go message: {msg!r}")
            return
        self.del_bubble()
        dx, dy = offset
        self.transfer_to(Coord(self.coord.x + dx, self.coord.y + dy))
        if self.on_move:
            self.on_move()

    # -------------------------------------------------------------- messaging

    def do(self, msg):
        if isinstance(msg, Say):
            self.say(msg.text)
        elif isinstance(msg, GoMessage):
            self.go(msg)
        else:
            logger.debug(f"{type(self).__name__} ignored message {msg!r}")

    def on_key_press(self, event: sdl.KeyboardEvent):
        super().on_key_press(event)
        msg_cls = _KEY_MESSAGES.get(event.key)
        if msg_cls is not None:
            self.do(msg_cls())