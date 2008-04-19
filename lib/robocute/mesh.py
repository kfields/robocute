
from pyglet.gl import *
from pyglet import graphics
    
class Mesh(object):
    def __init__(self, usage = 'dynamic'):
        super(Mesh, self).__init__()
        self.usage = usage
    
    def from_image(self, img):
        self.texture = img.get_texture(True) #is rectangle

    def draw(self, graphics):
        g = graphics
        t = self.texture.tex_coords
        x1 = g.x
        y1 = g.y
        x2 = x1 + self.texture.width
        y2 = y1 + self.texture.height
        z = g.z
        array = (GLfloat * 32)(
             t[0],  t[1],  t[2],  1.,
             x1,    y1,    z,     1.,
             t[3],  t[4],  t[5],  1., 
             x2,    y1,    z,     1.,
             t[6],  t[7],  t[8],  1., 
             x2,    y2,    z,     1.,
             t[9],  t[10], t[11], 1., 
             x1,    y2,    z,     1.)

        glPushAttrib(GL_ENABLE_BIT)
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
        glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
        glInterleavedArrays(GL_T4F_V4F, 0, array)
        glDrawArrays(GL_QUADS, 0, 4)
        glPopClientAttrib()
        glPopAttrib()
