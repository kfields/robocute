
import pyglet
from pyglet.gl import *

from vu import *

GROUP_TEXTURE = 0
GROUP_ATLAS = 1
GROUP_BIN = 2
'''
TextureGroup
'''
class TextureGroup(pyglet.graphics.Group):
    def __init__(self, texture, blend_src = GL_SRC_ALPHA, blend_dest = GL_ONE_MINUS_SRC_ALPHA, parent=None):
        super().__init__(parent)
        self.texture = texture
        self.blend_src = blend_src
        self.blend_dest = blend_dest

    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPushAttrib(GL_COLOR_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)

    def unset_state(self):
        glPopAttrib()
        glDisable(self.texture.target)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.texture.target == other.texture.target and
                self.texture.id == other.texture.id and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest)

    def __hash__(self):
        return hash((id(self.parent),
                     self.texture.id, self.texture.target,
                     self.blend_src, self.blend_dest))

'''
TextureStripGroup
'''
class TextureStripGroup(pyglet.graphics.Group):
    def __init__(self, strip, blend_src = GL_SRC_ALPHA, blend_dest = GL_ONE_MINUS_SRC_ALPHA, parent=None):
        super().__init__(parent)
        self.strip = strip
        self.texture = strip.texture
        self.blend_src = blend_src
        self.blend_dest = blend_dest

    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPushAttrib(GL_COLOR_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)

    def unset_state(self):
        glPopAttrib()
        glDisable(self.texture.target)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.texture.target == other.texture.target and
                self.texture.id == other.texture.id and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest)

    def __hash__(self):
        return hash((id(self.parent),
                     self.texture.id, self.texture.target,
                     self.blend_src, self.blend_dest))


class TextureStrip:
    def __init__(self, childWidth = 256, childHeight = 256, maxChildren = 20):
        self.childWidth = childWidth
        self.childHeight = childHeight
        self.width = childWidth * maxChildren
        self.height = childHeight
        
        self.texture = pyglet.image.Texture.create(
            self.width, self.height, pyglet.gl.GL_RGBA, rectangle=True)
        #
        self.celX = 0
        self.celY = 0
        #
        self.textures = {}
        
    def register(self, imgSrc, img):
        if not imgSrc in self.textures:
            texture = self.add(img)            
            self.textures[imgSrc] = texture
        #else
        texture = self.textures[imgSrc]
        return texture
            
    def add(self, img):
        x, y = self.alloc(img.width, img.height)
        self.texture.blit_into(img, x, y, 0)
        region = self.texture.get_region(x, y, img.width, img.height)
        return region

    def alloc(self, width, height):
        self.celX += width
        return self.celX, self.celY