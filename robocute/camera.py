from graphics import *

class Camera(Clip):
    
    def __init__(self, win):
        super().__init__()
        self.window = win
        #
        self.focalX = 0
        self.focalY = 0
        self.focalZ = 0
        #
        self.deviceWidth = win.width
        self.deviceHeight = win.height
        @win.event
        def on_resize(width, height):
            self.deviceWidth = width
            self.deviceHeight = height
            self.validate()            
        #
        self.graphics = Graphics()
        #self.validate()
    
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
