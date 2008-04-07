#lib
from camera import *
from mouse import *
#pyglet
from pyglet.window import key
#system
import sys

from robo.message import *
from node import *

fudge = (50, 50) #fixme:hack for camera

class User():
    def __init__(self, scene):
        self.scene = scene
        self.avatar = scene.create_avatar("RoboBoy") #avatar is the brain!!!
        self.avatar.start()
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
        self.camera.look_at(t[0] + fudge[0], t[1] + fudge[1])
        #
        win.set_mouse_visible(False)
        self.mouse = Mouse()
        self.scene.add_mouse(self.mouse)
        self.events = []
        #
        def on_avatar_move():
            block = self.scene.get_top_block_at(self.avatar.coord)
            t = self.scene.get_block_transform(block, self.avatar.coord)
            self.camera.look_at(t[0] + fudge[0], t[1] + fudge[1])
            
            
        self.avatar.on_move = on_avatar_move
        
        def on_key_press(symbol, modifiers):
            if symbol == key.ESCAPE:
                sys.exit()
            elif symbol == key.R:
                #self.avatar.do(Transition('start'))
                self.avatar.do(Transition('main'))
            #
            elif symbol == key.W:
                self.avatar.do(GoNorth())
            elif symbol == key.D:
                self.avatar.do(GoEast())
            elif symbol == key.S:
                self.avatar.do(GoSouth())
            elif symbol == key.A:
                self.avatar.do(GoWest())
            
        win.on_key_press = on_key_press

        def on_mouse_motion(x, y, dx, dy):
            self.mouse.x = x
            self.mouse.y = y

        win.on_mouse_motion = on_mouse_motion

        def on_mouse_press(x, y, button, modifiers):
            self.inject(MousePressed(x, y, button, modifiers))
        
        win.on_mouse_press = on_mouse_press
    
    def inject(self, event):
        if(not self.events):
            self.events = []
        self.events.append(event)
                           
    def dispatch_events(self):
        self.window.dispatch_events()
        query = None
        if(self.events):
            query = MouseQuery(self.events)
            self.events = None
        return query
    
    def get_camera(self):
        return self.camera
    