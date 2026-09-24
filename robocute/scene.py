from crunge.engine.d2.scene import Scene2D
from crunge.engine.d2.scene.layer import GraphLayer2D

from robocute.node import *
from robocute.world import *
from robocute.ui import *
from robocute import globe


class BubbleLayer(GraphLayer2D):
    def __init__(self, name):
        super().__init__(name)


class GameScene(Scene2D):

    def __init__(self, world, app):
        super().__init__()
        self.world = world
        self.app = app
        globe.scene = self
        #
        # self.bgImg = image.load(data.filepath('image/clouds.png'))
        #
        self.query = None

    def _create(self):
        super()._create()
        self.bubbles = self.add_layer(BubbleLayer("bubbles"))

    def _enable(self):
        super()._enable()
        self.primary_layer.attach(self.world)

    def draw_background(self, graphics):
        bgWidth = self.bgImg.width
        bgHeight = self.bgImg.height

        blitY = 0
        while blitY < self.window.height:
            blitX = 0
            while blitX < self.window.width:
                self.bgImg.blit(blitX, blitY, 0)
                blitX = blitX + bgWidth
            blitY = blitY + bgHeight

    def draw_world(self):
        self.draw_grids()

    def draw_grids(self):
        clip = self.clip
        #
        # gridColMax = self.node.gridColMax
        gridColMax = 10
        # gridRowMax = self.node.gridRowMax
        gridRowMax = 10

        #
        gridWidth = gridColMax * BLOCK_WIDTH
        invGridWidth = 1.0 / gridWidth
        gridHeight = gridRowMax * BLOCK_ROW_HEIGHT
        invGridHeight = 1.0 / gridHeight
        #
        posX = clip.gridX * gridWidth
        posY = clip.gridY * gridHeight
        #
        bottom = clip.bottom - posY
        top = clip.top - posY
        left = clip.left - posX
        right = clip.right - posX
        #
        rowCount = clip.rowCount
        rowMax = rowCount - 1
        colCount = clip.colCount
        colMax = colCount - 1
        #
        r1 = int(top * invGridHeight)
        if r1 < 0:
            r1 = 0
        if r1 > rowMax:
            r1 = rowMax
        #
        r2 = int(bottom * invGridHeight)
        if r2 < 0:
            r2 = 0
        if r2 > rowMax:
            r2 = rowMax
        #
        c1 = int(left * invGridWidth)
        if c1 < 0:
            c1 = 0
        if c1 > colMax:
            c1 = colMax
        #
        c2 = int(right * invGridWidth)
        if c2 < 0:
            c2 = 0
        if c2 > colMax:
            c2 = colMax
        #
        r = r1
        while r >= r2:  # rows in sheet
            row = clip.data[r]
            if len(row) == 0:
                c += 1
                continue
            c = c1
            blitY = posY + (r * gridHeight)
            while c <= c2:  # cells in row
                blitX = posX + (c * gridWidth)
                grid = row[c]
                if not grid:
                    # c += 1
                    clip.cache_miss(c, r)
                    continue
                # else
                self.draw_grid(grid, blitX, blitY, 1.0)
                c += 1
            r -= 1
        #
        # glPopMatrix()

    def draw_grid(self, grid, tX, tY, tZ=1.0):
        grid.draw()

    """
    Bubbles:
    """

    def add_bubble(self, bubble):
        self.bubbles.attach(bubble)

    def remove_bubble(self, bubble):
        self.bubbles.detach(bubble)

    """
    Mouse Support
    """

    def add_mouse(self, mouse):
        self.mice.add_node(mouse)

    def remove_mouse(self, mouse):
        self.mice.remove_node(mouse)
