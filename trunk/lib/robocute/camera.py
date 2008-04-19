from graphics import *

class Camera(Clip):
    
    def __init__(self, x = 0, y = 0, z = 0, width = 640, height = 480):
        super(Camera, self).__init__(x, y, z, width, height)
        #
        self.focalX = x
        self.focalY = y
        self.focalZ = z
        #
        self.deviceWidth = width
        self.deviceHeight = height
        #
        self.graphics = Graphics()
    
    def look_at(self, x, y, z = 0):
        self.focalX = x
        self.focalY = y
        self.focalZ = z
        self.validate()
        
    def zoom(self, zoomX, zoomY, zoomZ = 1.):
        g = self.graphics
        g.scale(g.scaleX + zoomX, g.scaleY + zoomY, 1.)
        self.validate()
        
    def validate(self):
        g = self.graphics
        clip = g.clip
        scaleX = g.scaleX
        scaleY = g.scaleY        
        invScaleX =  1 / scaleX
        invScaleY =  1 / scaleY
        #
        self.width = int(self.deviceWidth * invScaleX)
        self.height = int(self.deviceHeight * invScaleY)
        #
        self.x = int(self.focalX - ( self.width * .5 ) )
        self.y = int(self.focalY - ( self.height * .5 ) )
        #
        self.left = self.x
        self.bottom = self.y
        self.top = self.bottom + self.height
        self.right = self.left + self.width               
        #
        clip.x = self.x
        clip.left = self.left
        clip.y = self.y
        clip.bottom = self.bottom        
        clip.top = self.top
        clip.right = self.right        
