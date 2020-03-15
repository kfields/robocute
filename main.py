#! /usr/bin/env python

import sys
import os

try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'robocute'))
    sys.path.insert(0, libdir)

from pyglet import window
from robocute.app import App

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption='RoboCute', resizable=True)
app = App(win)
app.run()