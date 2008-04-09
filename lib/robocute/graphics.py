
import copy

from pyglet.gl import *

class Graphics(object):
    def __init__(self):
        super(Graphics, self).__init__()
        #
        self.x = 0
        self.y = 0
        self.z = 0
        self.width = 640
        self.height = 480
        #
        self.clipX = 0
        self.clipY = 0
        self.clipWidth = 640
        self.clipHeight = 480
        #
        self.color=(255.,255.,255.,1.)
        #
        #self.events = None
        self.query = None

    def copy(self):
        return copy.copy(self)

    def deep_copy(self):
        return copy.deepcopy(self)
    
    def translate(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z
        
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
    def project(self, x, y, z=0):
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
    def unproject(self, wx, wy, wz=0):
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
    '''
    Event Processing
    ...
    Okay this is all crazy and probably temporary.
    Were going to piggy back mouse events on the draw calls.
    Reason being ... I don't like maintaining positions on the objects
    '''

    
    def visit(self, vu):
        if(not vu.clickable): #temporary hack
            return
        query = self.query
        if(not query):
            return
        pos = self.unproject(query.x, query.y)
        if(pos[0] > self.x and pos[0] < self.x + vu.width):
            if(pos[1] > self.y and pos[1] < self.y + vu.height):
                query.result.append(vu.node)
                        