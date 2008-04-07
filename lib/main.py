'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
import sys
import os
#
import data

from robocute.scene import Scene

from pyglet import clock
from pyglet import window
from pyglet import font

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def main():
    #print "Hello from RoboCute main()!"
    #
    win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption='RoboCute')
    #
    #scene = Scene(win, "RoboCute.ods")
    scene = Scene(win, "RoboCuteFountain.ods")
    #scene = Scene(win, "RoboCuteHuge.ods")
    #scene = Scene(win, "RoboCuteDebug.ods")
    #scene = Scene(win, "RoboCuteSpawnDebug.ods")
    #scene = Scene(win, "RoboCuteTreasureDebug.ods")
    #
    user = scene.get_user()
    camera = user.get_camera()
    #
    #Create a font for our FPS clock
    ft = font.load('Verdana', 28)
    #
    fps_text = font.Text(ft, y=10, x=WINDOW_WIDTH - 200)
    #
    while not win.has_exit:
        query = user.dispatch_events()
        #
        if(query):
           camera.query = query
        #
        dt = clock.tick()
        #
        win.clear()
        #
        scene.draw(camera)
        #
        if(query):
            query.process()
        #
        camera.query = None
        #
        fps_text.text = ("fps: %d") % (clock.get_fps())
        fps_text.draw()        
        #
        win.flip()
    