from graphics import *

class Camera(Graphics):
    
    def __init__(self, scene):
        super(Camera, self).__init__()
        
    def look_at(self, x, y):        
        tX = x - ( self.width * .5)
        tY = y - ( self.height * .5)
        #
        self.translate(tX, tY)
        #
        self.clipX = tX
        self.clipY = tY
