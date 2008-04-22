
import pyglet
from pyglet.gl import *

from vu import *
from texture import *

'''
TileStrip
'''

class TileStrip(TextureStrip):
    instance = None    
    instanced = None
    def __new__(cls, *args, **kargs):
        instance = cls.instance
        if not instance:
            obj = object.__new__(cls)
            instance = obj
            cls.instance = obj            
            obj.__init__(*args, **kargs)
        return instance
    
    def __init__(self):
        if self.instanced:
            return
        super(TileStrip, self).__init__(childWidth = 101, childHeight = 171)
        self.instanced = True

class TileVu(ImageVu):
    def __init__(self, node, imgSrc):
        super(TileVu, self).__init__(node, imgSrc)
        #self.texture = self.image.get_texture(True) #is rectangle
        self.strip = TileStrip()
        #self.texture = self.strip.add(self.image) 
        self.texture = self.strip.register(self.imgSrc, self.image)
        
    def validate(self):
        super(TileVu, self).validate()

    def create_array(self, g):
        x1 = g.x
        y1 = g.y
        x2 = x1 + self.texture.width
        y2 = y1 + self.texture.height
        z = g.z
        t = self.texture.tex_coords        
        array = (GLfloat * 32)(
             t[0],  t[1],  t[2],  1.,
             x1,    y1,    z,     1.,
             t[3],  t[4],  t[5],  1., 
             x2,    y1,    z,     1.,
             t[6],  t[7],  t[8],  1., 
             x2,    y2,    z,     1.,
             t[9],  t[10], t[11], 1., 
             x1,    y2,    z,     1.)
        return array
    
    def create_vertices(self, g):
        x1 = g.x
        y1 = g.y
        x2 = x1 + self.texture.width
        y2 = y1 + self.texture.height        
        vertices = [x1, y1, x2, y1, x2, y2, x1, y2]
        return vertices
        
    def create_texture_coords(self):
        texture = self.texture 
        x = texture.x
        y = texture.y
        z = texture.z
        width = texture.width
        height = texture.height
        #
        owner = texture.owner
        owner_u1 = owner.tex_coords[0]
        owner_v1 = owner.tex_coords[1]
        owner_u2 = owner.tex_coords[3]
        owner_v2 = owner.tex_coords[7]
        scale_u = owner_u2 - owner_u1
        scale_v = owner_v2 - owner_v1
        u1 = x / float(owner.width) * scale_u + owner_u1
        v1 = y / float(owner.height) * scale_v + owner_v1
        u2 = (x + width) / float(owner.width) * scale_u + owner_u1
        v2 = (y + height) / float(owner.height) * scale_v + owner_v1
        r = z / float(owner.images) + owner.tex_coords[2]
        tex_coords = (u1, v1, r, u2, v1, r, u2, v2, r, u1, v2, r)
        return tex_coords
        
    def draw(self, g):
        array = self.create_array(g)
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        glInterleavedArrays(GL_T4F_V4F, 0, array)
        glDrawArrays(GL_QUADS, 0, 4)
        glPopClientAttrib()
        glPopAttrib()
        #
        if g.query:
            self.query(g)
            
    def batch(self, g):
        layer = g.layer
        group = layer.register_group(TextureStripGroup(self.strip))
        batchLayer = g.layer.root
        #group = None
        #batchLayer = g.layer
        batch = batchLayer.batch
        tex_coords = self.texture.tex_coords
        #tex_coords = self.create_texture_coords()
        vertexList = batch.add(4, GL_QUADS, group,
            'v2i/%s' % 'dynamic', 
            'c4B', ('t3f', tex_coords))
        vertices = self.create_vertices(g)
        vertexList.vertices[:] = vertices
        #self._vertex_list.colors[:] = [r, g, b, int(self._opacity)] * 4
        vertexList.colors[:] = [255, 255, 255, 255] * 4



        