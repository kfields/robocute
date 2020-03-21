
from robocute.keyboard import *
from robocute.mouse import *
from robocute.brain import *

class ToolKeybox(Keybox):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain

    def on_key_press(self, symbol, modifiers):
        brain = self.brain
        user = brain.user
        if symbol == key.ESCAPE:
            user.pop_tool()
        else:
            super().on_key_press(symbol, modifiers)

class ToolMousebox(Mousebox):    
    def __init__(self, brain):
        super().__init__()
        self.brain = brain

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        self.brain.scene.query = MouseQuery(MousePressed(x, y, button, modifiers))

class Tool(Brain):
    def __init__(self, dna = None):
        super().__init__(None) #no node ...
