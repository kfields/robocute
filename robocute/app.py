import sys
import os
from random import seed
#
import pyglet
from pyglet import clock
from pyglet import window
#
import data
from robocute.game.default import DefaultGame
from robocute.world import World
from robocute.scene import Scene
from robocute.graphics import Graphics
#
from robocute.user import *
#
class App:
    
    def __init__(self, win, game_name = 'Default'):
        self.window = win                
        #
        game = self.load_or_create_game(game_name)
        self.game = game
        self.catalog = game.catalog
        self.world = game.world
        self.scene = game.scene
        #
        self.callbacks = []
        #
        self.user = None
        self.homes = []
        #
        self.isRunning = False
    
    def load_or_create_game(self, game_name):
        game = self.load_game(game_name)
        if not game:
            game = self.create_game(game_name)
        return game
    
    def load_game(self, game_name):
        game = None
        return game
        
    def create_game(self, game_name):
        game = DefaultGame(self, game_name) #fixme: Need game factory ...
        return game
    
    def save_game(self):
        self.game.save()

    def on_run(self):
        seed()
        self.user = self.create_user()
        self.isRunning = True
        #
        #Create our FPS clock
        self.fps_text = pyglet.text.Label('0',
                                font_name='Verdana',
                                font_size=28,
                                x=self.window.width - 200, y=10)
    def exit(self):
        self.isRunning = False
        self.on_exit()
        
    def on_exit(self):
        self.game.save()
        
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
    '''
    def add_home(self, home, coord):
        self.homes.append(coord)
            
    def run(self):
        self.on_run()
        #
        '''
        while not self.window.has_exit and self.isRunning:
            self.update()
        '''
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()
 
    def update(self, dt):
        win = self.window
        scene = self.scene
        user = self.user
        fps_text = self.fps_text
        #
        worldGraphics = user.camera.graphics
        layerGraphics = Graphics()
        #
        #user.dispatch_events()
        #
        dt = clock.tick()
        #
        #win.clear()
        #
        scene.draw(layerGraphics, worldGraphics)
        #
        #fps_text.text = ("fps: %d") % (clock.get_fps())
        #fps_text.draw()        
        #
        #win.flip()
        #
        if len(self.callbacks) != 0:
            for callback in self.callbacks:
                callback()
            self.callbacks = []
