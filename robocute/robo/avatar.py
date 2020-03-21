
from robocute.tool import *

from message import *

class AvatarKeybox(ToolKeybox):
    def __init__(self, brain):
        super().__init__(brain)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.R:
            #self.brain.do(Transition('start'))
            self.brain.do(Transition('main'))
        if symbol == key.W or symbol == key.UP:
            self.brain.do(GoNorth())
        elif symbol == key.D or symbol == key.RIGHT:
            self.brain.do(GoEast())
        elif symbol == key.S or symbol == key.DOWN:
            self.brain.do(GoSouth())
        elif symbol == key.A or symbol == key.LEFT:
            self.brain.do(GoWest())
        else:
            super().on_key_press(symbol, modifiers)

class AvatarMousebox(ToolMousebox):    
    def __init__(self, brain):
        super().__init__(brain)
