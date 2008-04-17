from graphics import *

class Camera(Graphics):
    
    def __init__(self, scene):
        super(Camera, self).__init__()
        self.focalX = 0
        self.focalY = 0
        self.focalZ = 0
    
    def look_at(self, x, y, z = 0):
        self.focalX = x
        self.focalY = y
        self.focalZ = z
        self.validate()
        
    def zoom(self, zoomX, zoomY, zoomZ = 1.):
        self.scale(zoomX, zoomY, zoomZ)
        self.validate()
        
    def validate(self):
        scaleX =  self.scaleX
        scaleY =  self.scaleY        
        invScaleX =  1 / scaleX
        invScaleY =  1 / scaleY
        #
        #tX = (x - ( self.width * .5)) * invScaleX
        tX = int((self.focalX - ( self.width * .5 * invScaleX)) * scaleX)
        #tY = (y - ( self.height * .5)) * invScaleY
        tY = int((self.focalY - ( self.height * .5 * invScaleY)) * scaleY)
        #
        self.translate(tX, tY)
        #
        self.clipX = tX
        self.clipY = tY        
