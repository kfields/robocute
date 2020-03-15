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

from robocute.wxauitest import TestApp

app = TestApp(redirect=False)
app.MainLoop()