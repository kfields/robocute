'''
There is no Tool class.  It's a role.
Any brain can be an Tool.
A 'physical' body is optional.
'''

from keyboard import *
from mouse import *

class ToolKeybox(Keybox):
    def __init__(self, brain):
        super(ToolKeybox, self).__init__()
        self.brain = brain

    def on_key_press(self, symbol, modifiers):
        brain = self.brain
        user = brain.user
        if symbol == key.ESCAPE:
            user.pop_tool()
        else:
            super(ToolKeybox, self).on_key_press(symbol, modifiers)

class ToolMousebox(Mousebox):    
    def __init__(self, brain):
        super(ToolMousebox, self).__init__()
        self.brain = brain

    def on_mouse_press(self, x, y, button, modifiers):
        super(ToolMousebox, self).on_mouse_press(x, y, button, modifiers)
        self.brain.scene.query = MouseQuery(MousePressed(x, y, button, modifiers))
