'''
There is no Avatar class.  It's a role.
Any brain can be an Avatar.
A 'physical' body is optional.
'''

from tool import *

from robo.message import *

class AvatarKeybox(ToolKeybox):
    def __init__(self, brain):
        super(AvatarKeybox, self).__init__(brain)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.R:
            #self.brain.do(Transition('start'))
            self.brain.do(Transition('main'))
        if symbol == key.W:
            self.brain.do(GoNorth())
        elif symbol == key.D:
            self.brain.do(GoEast())
        elif symbol == key.S:
            self.brain.do(GoSouth())
        elif symbol == key.A:
            self.brain.do(GoWest())
        else:
            super(AvatarKeybox, self).on_key_press(symbol, modifiers)

class AvatarMousebox(ToolMousebox):    
    def __init__(self, brain):
        super(AvatarMousebox, self).__init__(brain)
