'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
import sys
import os
from random import seed
#
from pyglet import clock
from pyglet import window
from pyglet import font
#
import data
from world import World
from scene import Scene
from graphics import Graphics
#
from user.player import *
from user.designer import *
#
#from robo.robo import Avatar
#
from builder import build

#WINDOW_WIDTH = 800
#WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

class App(object):
    
    def __init__(self, filename):
        self.filename = filename
        self.world = self.create_world()
        #
        self.window = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption='RoboCute')                
        self.scene = Scene(self.world, self, self.window)
        self.world.vu = self.scene
        #
        self.callbacks = []
        #
        self.user = None
        self.homes = []
    
    def create_world(self):
        world = World(self, self.filename)
        return world
        
    def build(self, text, coord, cell, item = None):
        return build(self, text, coord, cell, item)
        
    def start(self):
        self.user = self.create_user()
    
    def create_user(self):
        user = User(self)
        #user = Designer(self)
        #user = Player(self)
        return user
        

    '''
    Callbacks
    '''
    def add_callback(self, callback):
        self.callbacks.append(callback)
    def remove_callback(self, callback):
        self.callbacks.remove(callback)
    '''
    Avatar Support
    fixme:this may need to go into User
    '''
    def add_home(self, home, coord):
        self.homes.append(coord)
        
    def create_avatar(self, text):
        if len(self.homes) != 0:
            home = self.homes[0] #fixme:multiple homes?
        else:
            home = Coord(0,0)

        cell = self.world.get_cell_at(home)
        node = self.build(text, home, cell)
        if(not node):
            raise Exception('No Avatar found in scene!!!')
        brain = node.get_brain()
        if(brain == None):
           raise Exception("This node has no brain!")
        #
        return brain
        
    def run(self):
        seed()
        win = self.window
        scene = self.scene
        self.start()        
        user = self.user
        camera = user.camera
        graphics = Graphics()
        #
        #Create a font for our FPS clock
        ft = font.load('Verdana', 28)
        #
        fps_text = font.Text(ft, y=10, x=WINDOW_WIDTH - 200)
        #
        #
        while not win.has_exit:
            #
            '''
            for callback in self.callbacks:
                callback()
            '''
            #
            query = user.dispatch_events()
            #
            if(query):
               camera.query = query
               graphics.query = query
            #
            dt = clock.tick()
            #
            win.clear()
            #
            scene.draw(graphics, camera)
            #
            if(query):
                query.process()
            #
            camera.query = None
            graphics.query = None
            #
            fps_text.text = ("fps: %d") % (clock.get_fps())
            fps_text.draw()        
            #
            win.flip()
            #
            if len(self.callbacks) != 0:
                for callback in self.callbacks:
                    callback()
                self.callbacks = []
