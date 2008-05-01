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
from game.default import DefaultGame
from world import World
from scene import Scene
from graphics import Graphics
#
from user import *
#
from builder import build

#WINDOW_WIDTH = 800
#WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

class App(object):
    
    def __init__(self, gameName = 'Default'):
        self.window = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption='RoboCute')                
        #
        game = self.create_game(gameName)
        self.game = game
        self.catalog = game.catalog
        self.world = game.world
        self.scene = game.scene
        #
        self.callbacks = []
        #
        self.user = None
        self.homes = []
        
    def create_game(self, gameName):
        game = DefaultGame(self, gameName) #fixme: Need game factory ...
        return game
            
    def build(self, text, coord, cell, item = None):
        return build(self, text, coord, cell, item)
        
    def start(self):
        self.user = self.create_user()
    
    def create_user(self):
        user = User(self)
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
        brain = node.brain
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
        worldGraphics = user.camera.graphics
        layerGraphics = Graphics()
        #
        #Create a font for our FPS clock
        ft = font.load('Verdana', 28)
        #
        fps_text = font.Text(ft, y=10, x=WINDOW_WIDTH - 200)
        #
        #
        while not win.has_exit:
            user.dispatch_events()
            #
            dt = clock.tick()
            #
            win.clear()
            #
            scene.draw(layerGraphics, worldGraphics)
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
