from typing import Optional

import glm

from crunge import yoga

from crunge.engine.d2.nine_patch.nine_patch import NinePatch, NinePatchFill
from crunge.engine.d2.nine_patch.nine_patch_vu import NinePatchVu
from crunge.engine.d2.control import Control2D, WidgetControl2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.d2.settings_2d import Settings2D
from crunge.engine.ui.flex import Row
from crunge.engine.widget import Widget

DEFAULT_SKIN = "${resources}/image/skin/SpeechBubble.png"

# Run find_insets.py on the image for the real values: the caps must contain
# the whole rounded corner, and anything left in an edge slice gets repeated
DEFAULT_INSETS = glm.vec4(0.45, 0.45, 0.45, 0.45)

# The bubble has a vertical gradient, so rows stretch and only columns tile
DEFAULT_FILL = NinePatchFill.TILE_X


class SpeechBubble(Control2D):
    """A nine-patch bubble that fits its content.

    The content is a flex container of widgets -- a Row by default -- carried
    into the scene by a WidgetControl2D. Yoga sizes the bubble from it: content
    plus padding equal to the nine-patch border, so it sits inside the rounded
    edge, floored at the border sum, below which the corners would overlap.

    When the bubble is a layout root it lays itself out, in _update. A bubble
    nested under another Control2D is laid out by that control's root instead,
    so it never calculates twice.

    Placement (root bubbles only): with `anchor` unset the bubble keeps its
    centered position and grows in every direction at once. Set `anchor` to a
    point in the parent's space and the bubble's lower-left corner stays pinned
    there, so it grows up and to the right as the content changes.
    """

    def __init__(
        self,
        items: list[Widget],
        spacing: float = 10,
        container: type[Widget] = Row,
        skin: str = DEFAULT_SKIN,
        insets: glm.vec4 = None,
        fill: NinePatchFill = DEFAULT_FILL,
        anchor: Optional[glm.vec2] = None,
    ):
        sprite = SpriteLoader().load(skin)
        self.patch = NinePatch.from_sprite(
            sprite,
            insets if insets is not None else DEFAULT_INSETS,
            fill=fill,
        )
        super().__init__(model=self.patch)
        self.add_chip(NinePatchVu())

        self.content = WidgetControl2D(container(children=items, spacing=spacing))
        self.add_child(self.content)

        self._anchor = glm.vec2(anchor) if anchor is not None else None

    def _create(self):
        super()._create()
        # The yoga node exists from here on.
        #
        # Each child at its natural width. A column stretches its children
        # across by default, which would widen the content to the bubble.
        self.layout.layout_node.set_align_items(yoga.Align.FLEX_START)
        self.apply_border()
        self._apply_anchor()

    # -- placement ---------------------------------------------------------

    @property
    def anchor(self) -> Optional[glm.vec2]:
        """Lower-left corner in the parent's space, or None to keep the center."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: Optional[glm.vec2]) -> None:
        self._anchor = glm.vec2(value) if value is not None else None
        self._apply_anchor()

    def _apply_anchor(self) -> None:
        # Nodes are centered and y-up, so the center sits half a size up and
        # right of the lower-left corner. `size` includes scale, which is what
        # a position in the parent's space needs.
        if self._anchor is not None:
            self.position = self._anchor + self.size * 0.5

    # -- style -------------------------------------------------------------

    @property
    def border(self) -> glm.vec4:
        """The nine-patch border as rendered, in world units: left, top,
        right, bottom."""
        # ASSUMPTION: border_zoom scales the rendered border linearly
        return (
            glm.vec4(self.patch.border_texels)
            / Settings2D().ppu
            * self.patch.border_zoom
        )

    def apply_border(self) -> None:
        """Pad the content clear of the border, and floor the size at it.

        Call again after changing the patch's insets or border_zoom: both move
        the border, and the layout doesn't observe the patch.
        """
        node = self.layout.layout_node
        border = self.border

        node.set_padding(yoga.Edge.LEFT, border.x)
        node.set_padding(yoga.Edge.TOP, border.y)
        node.set_padding(yoga.Edge.RIGHT, border.z)
        node.set_padding(yoga.Edge.BOTTOM, border.w)

        # A nine-patch has no natural size, only a minimum: any smaller and
        # the corners collide. That's its real opinion, so it's a floor rather
        # than an intrinsic size.
        node.set_min_width(border.x + border.z)
        node.set_min_height(border.y + border.w)

    # -- frame -------------------------------------------------------------

    def _update(self, delta_time):
        # Only as a root: a nested bubble is laid out by its root's pass.
        # calculate() early-returns when nothing is dirty, so this is a flag
        # check most frames. Bare calculate() fits to content, same as the
        # demo relies on.
        if self.layout.is_root and self.layout.stale:
            self.layout.calculate()
            self.layout.apply()
            # The pass may have changed the size; re-pin the corner.
            self._apply_anchor()
        super()._update(delta_time)