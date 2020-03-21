#! /usr/bin/env python

import sys
import os

sys.path.append(os.path.abspath(__file__))

from pyglet import window
from robocute.app import App

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption='RoboCute', resizable=True)
app = App(win)
app.run()