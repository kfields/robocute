from crunge import skia
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.vu import Vu as CrungeVu
from robocute.base import *
from robocute.graphics import Graphics

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
    def __init__(self, node):
        super().__init__()
        self.width = None
        self.height = None
        self.hotspots = []
        #
        # query support
        self.hotHeight = 0

    def draw(self, graphics):
        pass

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
    def __init__(self, node):
        super().__init__(node)
        self.text = pyglet.text.Label(
            self.node.text, font_name="Verdana", font_size=14, color=(0, 0, 0, 255)
        )
        self.validate()
        self.add_hotspot(HotSpot(0, 0, self.width, self.height))  # fixme:put in base?

    def validate(self):
        super().validate()
        # self.width = self.text.width
        self.width = self.text.content_width
        # self.height = self.text.height
        self.height = self.text.content_height

    def draw(self, graphics):
        # super().draw(graphics)
        # either way works...
        # glPushMatrix()
        # glTranslatef(graphics.x, graphics.y, graphics.z)
        self.text.x = graphics.x
        self.text.y = graphics.y
        self.text.draw()
        # glPopMatrix()
        if graphics.query:
            self.query(graphics)


class ImageVu(Vu):
    def __init__(self, node, imgSrc):
        super().__init__(node)
        self.imgSrc = imgSrc

        path = ResourceManager().resolve_path("${resources}/image/" + imgSrc)
        info = skia.ImageInfo()
        data = skia.Data.make_from_file_name(str(path))
        image = skia.deferred_from_encoded_data(data)

        if imgSrc != "":
            self.image = image
        else:
            self.image = None
        self.add_hotspot(
            HotSpot(0, 0, self.width, self.hotHeight)
        )  # fixme:put in base?

    def plug(self):
        super().plug()
        if not self.width:
            self.width = self.image.width
        if not self.height:
            self.height = self.image.height
        # query support
        self.hotHeight = self.height
        # hack?
        self.node.z = self.width

    def draw(self, graphics):
        if self.image:
            self.image.blit(graphics.x, graphics.y, graphics.z)
        if graphics.query:
            self.query(graphics)
