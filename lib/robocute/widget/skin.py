
import data

from robocute.graphics import *

from pyglet import image

def load_slice(filename):
    return image.load(data.filepath('image/' + filename))

class AbstractSkin(object):
    def __init__(self, slicesName, sliceCount):
        self.slicesName = slicesName
        self.sliceCount = sliceCount
        self.slices = [None] * sliceCount
        #
        self.height = 5
        self.width = 5
        #
        self.margin_top = 5
        self.margin_bottom = 5        
        self.margin_left = 5
        self.margin_right = 5        
        #
        imgCount = 0
        
        while(imgCount != sliceCount):
            self.slices[imgCount] = load_slice(slicesName + '_0' + str(imgCount+1) + '.png')
            imgCount += 1
        #
        self.validate()

    def validate(self):
        pass
    
    def draw(self, graphics):
        pass
    
class HorizontalSkin(AbstractSkin):
    def __init__(self, slicesName):
        super(HorizontalSkin, self).__init__(slicesName, 3)

    def validate(self):
        self.width = 0
        self.height = self.slices[0].height
        #
        self.margin_left = self.slices[0].width
        self.width += self.margin_left 
        self.margin_right = self.slices[2].width
        self.width += self.margin_right

    def draw(self, graphics):
        #home slice
        self.slices[0].blit(graphics.x, graphics.y, graphics.z)
        blitLeft = graphics.x + self.margin_left
        blitRight = blitLeft + ( graphics.width - self.margin_right)
        graphics.x = blitLeft
        
        scissor = graphics.project(graphics.x, graphics.y)
        scissorX = GLint(int(scissor[0])) #only way!!!
        scissorY = GLint(int(scissor[1]))

        scissorW = int((graphics.width - self.margin_right) * graphics.scaleX)
        scissorH = int(graphics.height * graphics.scaleY)
        #
        glEnable(GL_SCISSOR_TEST)
        glScissor(scissorX, scissorY, scissorW, scissorH)
        #
        while(graphics.x <= blitRight):
            self.slices[1].blit(graphics.x, graphics.y, graphics.z)
            graphics.x += self.slices[1].width
        #
        glDisable(GL_SCISSOR_TEST)
        #end slice
        graphics.x = blitRight
        self.slices[2].blit(graphics.x, graphics.y, graphics.z)

class VerticalSkin(AbstractSkin):
    def __init__(self, slicesName):
        super(VerticalSkin, self).__init__(slicesName, 3)

    def validate(self):
        self.height = 0
        self.width = self.slices[0].width
        #
        self.margin_top = self.slices[0].height
        self.height += self.margin_top 
        self.margin_bottom = self.slices[2].height
        self.height += self.margin_bottom

    def draw(self, graphics):
        #bottom slice
        self.slices[0].blit(graphics.x, graphics.y, graphics.z)
        blitBottom = graphics.y + self.margin_bottom
        blitTop = blitBottom + ( graphics.height - self.margin_top)
        graphics.y = blitBottom
        #middle slice
        scissor = graphics.project(graphics.x, graphics.y)
        scissorX = GLint(int(scissor[0])) #only way!!!
        scissorY = GLint(int(scissor[1]))
        #scissorW = self.width
        #scissorH = self.height + self.margin_top + 1
        scissorW = int(graphics.width * graphics.scaleX)
        scissorH = int((graphics.height - self.margin_top) * graphics.scaleY)
                
        glEnable(GL_SCISSOR_TEST)
        glScissor(scissorX, scissorY, scissorW, scissorH)
        #
        while(graphics.y <= blitTop ):
            self.slices[1].blit(graphics.x, graphics.y, graphics.z)
            graphics.y += self.slices[1].height
        #
        glDisable(GL_SCISSOR_TEST)
        #end slice
        #self.slices[2].blit(graphics.x, graphics.y, graphics.z)
        self.slices[2].blit(graphics.x, blitTop, graphics.z)
