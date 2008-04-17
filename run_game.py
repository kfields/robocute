#! /usr/bin/env python

import sys
import os

try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    sys.path.insert(0, libdir)

#import main
#main.main()
from robocute.game import Game

#filename = "Default.ods"
#filename = "Fountain.ods"
#filename = "Debug.ods"
#filename = "SpawnDebug.ods"
#filename = "TreasureDebug.ods"
#filename = "SpreaderDebug.ods"
filename = "TreasureTile.ods"

game = Game('grid/' + filename)
game.run()