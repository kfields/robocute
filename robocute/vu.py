from loguru import logger

from crunge import skia
from crunge.engine.renderer import Renderer
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.vu import Vu as CrungeVu
from robocute.base import *

"""
HotSpot : Just a way to clip events right now.  More in the future.
"""


class HotSpot:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Vu(CrungeVu):
    def __init__(self):
        super().__init__()
        self.width = None
        self.height = None
        self.hotspots = []
        #
        # query support
        self.hotHeight = 0

    def batch(self, g):
        pass

    def add_hotspot(self, hotspot):
        self.hotspots.append(hotspot)

    def remove_hotspot(self, hotspot):
        self.hotspots.remove(hotspot)

    def has_hotspots(self):
        return len(self.hotspots) != 0

    def query(self, g):
        query = g.query
        if not query:
            return
        if not self.has_hotspots():  # temporary hack
            return
        pos = g.unproject(query.x, query.y)
        for hotspot in self.hotspots:
            hotX1 = g.x + hotspot.x
            hotY1 = g.y + hotspot.y
            hotX2 = hotX1 + hotspot.width
            hotY2 = hotY1 + hotspot.height
            if pos[0] > hotX1 and pos[0] < hotX2:
                if pos[1] > hotY1 and pos[1] < hotY2:
                    query.add_result(self.node, g.cellX, g.cellY, g.cellZ)


class TextVu(Vu):
    def __init__(self):
        super().__init__()
        '''
        self.text = pyglet.text.Label(
            self.node.text, font_name="Verdana", font_size=14, color=(0, 0, 0, 255)
        )
        '''
        #self.validate()
        self.add_hotspot(HotSpot(0, 0, self.width, self.height))  # fixme:put in base?

    def validate(self):
        super().validate()
        # self.width = self.text.width
        self.width = self.text.content_width
        # self.height = self.text.height
        self.height = self.text.content_height

class ImageVu(Vu):
    def __init__(self, img_src):
        super().__init__()
        self.img_src = img_src
        logger.debug(f"ImageVu initialized with img_src: {img_src}")

        path = ResourceManager().resolve_path("${resources}/image/" + img_src)
        data = skia.Data.make_from_file_name(str(path))
        self.image = skia.deferred_from_encoded_data(data)

    def _draw(self):
        #logger.debug(f"Drawing ImageVu with img_src: {self.img_src}")
        canvas = Renderer.get_current().canvas
        #position = self.node.global_position
        position = self.node.global_position
        #logger.debug(f"Drawing ImageVu at position: {position}")
        canvas.draw_image(self.image, position.x, position.y)
        super()._draw()

class BubbleVu(Vu):
    def __init__(self):
        super().__init__()

    def _draw(self):
        canvas = Renderer.get_current().canvas
        w, h = self.node.size
        #w, h = self.node.layout.width, self.node.layout.height
        rect = skia.Rect.MakeWH(w, h)
        rrect = skia.RRect.MakeRectXY(rect, 12, 12)

        fill = skia.Paint(Color=skia.ColorWHITE, AntiAlias=True)
        canvas.draw_r_rect(rrect, fill)

        stroke = skia.Paint(
            Color=skia.ColorSetARGB(255, 60, 60, 70),
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=2,
            AntiAlias=True,
        )
        canvas.draw_r_rect(rrect, stroke)
        super()._draw()
