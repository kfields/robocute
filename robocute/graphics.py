
from pyglet.gl import *

from shape import *

class Clip(Rect):
    def __init__(self, x = 0, y = 0, z = 0, width = 0, height = 0):
        super(Clip, self).__init__(x, y, z, width, height)
        self.top = y + height
        self.left = x
        self.bottom = y
        self.right = x + width

class Graphics(Rect):
    def __init__(self, x = 0, y = 0, z = 0, width = 0, height = 0):
        super(Graphics, self).__init__(x, y, z, width, height)
        #
        self.scaleX = 1.
        self.scaleY = 1.
        self.scaleZ = 1.
        #
        self.color=(255.,255.,255.,1.)
        #
        #now it's really getting nuts.
        self.cellX = 0
        self.cellY = 0        
        self.cellZ = 0
        self.query = None
        
        #
        self.clip = Clip(self.x, self.y, self.width, self.height)
        #
        self.batch = None
        self.layer = None
    
    def translate(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def scale(self, scaleX, scaleY, scaleZ = 1.):
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.scaleZ = scaleZ
        
    def set_color(self,c):
        self.color = c

    #model to screen
    '''
    C SPECIFICATION
      GLint    gluProject( GLdouble objX,
                GLdouble objY,
                GLdouble objZ,
                const GLdouble *model,
                const GLdouble *proj,
                const GLint    *view,
                GLdouble* winX,
                GLdouble* winY,
                GLdouble* winZ )    
    '''
    def project(self, x, y, z = 0):
        viewport = (GLint * 4)()
        mvmatrix = (GLdouble * 16)()
        projmatrix = (GLdouble * 16)()
        glGetIntegerv(GL_VIEWPORT, viewport)
        glGetDoublev(GL_MODELVIEW_MATRIX, mvmatrix)
        glGetDoublev(GL_PROJECTION_MATRIX, projmatrix)
        wx = GLdouble()
        wy = GLdouble()
        wz = GLdouble()
        gluProject(x, y, z, mvmatrix, projmatrix, viewport, wx, wy, wz)
        return (wx.value, wy.value, wz.value)
    
    #screen to model
    '''
    C SPECIFICATION
      GLint    gluUnProject( GLdouble winX,
                  GLdouble winY,
                  GLdouble winZ,
                  const GLdouble *model,
                  const GLdouble *proj,
                  const GLint *view,
                  GLdouble*    objX,
                  GLdouble*    objY,
                  GLdouble*    objZ )    
    '''
    def unproject(self, wx, wy, wz = 0):
        viewport = (GLint * 4)()
        mvmatrix = (GLdouble * 16)()
        projmatrix = (GLdouble * 16)()
        glGetIntegerv(GL_VIEWPORT, viewport)
        glGetDoublev(GL_MODELVIEW_MATRIX, mvmatrix)
        glGetDoublev(GL_PROJECTION_MATRIX, projmatrix)
        x = GLdouble()
        y = GLdouble()
        z = GLdouble()
        gluUnProject(wx, wy, wz, mvmatrix, projmatrix, viewport, x, y, z)
        return (x.value, y.value, z.value)
