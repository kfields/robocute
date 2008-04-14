#lib
from robocute.camera import *
from robocute.mouse import *
#pyglet
from pyglet.window import key
#system
import sys

from robocute.robo.message import *
from robocute.node import *
from robocute.block.block import *

#fudge = (50, 50) #fixme:hack for camera
fudge = (BLOCK_WIDTH * .5, BLOCK_HEIGHT * .5) #fixme:hack for camera

class User(object):
    def __init__(self, scene):
        self.scene = scene
        self.avatar = scene.create_avatar("RoboBoy") #avatar is the brain!!!
        #
        self.camera = Camera(scene)
        win = scene.window
        self.window = win
        #
        self.camera.width = win.width
        self.camera.height = win.height
        self.camera.clipWidth = win.width
        self.camera.clipHeight = win.height        
        #
        #better to just focus on the ground
        block = self.scene.get_top_block_at(self.avatar.coord)
        t = self.scene.get_block_transform(block, self.avatar.coord)
        self.camera.look_at(t.x + fudge[0], t.y + fudge[1])
        #
        win.set_mouse_visible(False)
        self.mouse = Mouse()
        self.scene.add_mouse(self.mouse)
        self.events = []
        #
        self.coord = Coord(0,0)        
        #
        def on_avatar_move():
            self.move_to(self.avatar.coord)                        
        self.avatar.on_move = on_avatar_move
        
        def on_key_press(symbol, modifiers):
            self.on_key_press(symbol, modifiers)            
        win.on_key_press = on_key_press

        def on_mouse_motion(x, y, dx, dy):
            self.on_mouse_motion(x, y, dx, dy)            
        win.on_mouse_motion = on_mouse_motion

        def on_mouse_press(x, y, button, modifiers):
            self.on_mouse_press(x, y, button, modifiers)        
        win.on_mouse_press = on_mouse_press

        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        win.on_mouse_drag = on_mouse_drag

    def on_key_press(self, symbol, modifiers):
        if symbol == key.NUM_ADD:
            self.camera.zoom(self.camera.scaleX + .1, self.camera.scaleY + .1)
        elif symbol == key.NUM_SUBTRACT:
            self.camera.zoom(self.camera.scaleX - .1, self.camera.scaleY - .1)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.x = x
        self.mouse.y = y

    def on_mouse_press(self, x, y, button, modifiers):
        self.inject(MousePressed(x, y, button, modifiers))
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse.x = x
        self.mouse.y = y
    
    def inject(self, event):
        if(not self.events):
            self.events = []
        self.events.append(event)
                           
    def dispatch_events(self):
        self.window.dispatch_events()
        query = None
        if(self.events):
            #query = MouseQuery(self.events)
            query = self.create_mousequery(self.events)
            self.events = None
        return query
    
    def create_mousequery(self, events):
        return MouseQuery(events)
    
    def get_camera(self):
        return self.camera
    
    def move_to(self, coord):
        self.coord = coord
        block = self.scene.get_top_block_at(coord)        
        t = self.scene.get_block_transform(block, coord) #fixme:this really needs to be fixed!
        self.camera.look_at(t.x + fudge[0], t.y + fudge[1])
        
    