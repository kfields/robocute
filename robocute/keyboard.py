
import sys

from pyglet.window import key

from mailbox import Mailbox

class Keybox(Mailbox):
    def __init__(self):
        super(Keybox, self).__init__()

    def exit(self):
        sys.exit()
        
    def on_key_press(self, symbol, modifiers):
        pass

class MultiKeybox(Mailbox):
    def __init__(self):
        super(MultiKeybox, self).__init__()
            
    def on_key_press(self, symbol, modifiers):
        for box in self.boxes:
            box.on_key_press(symbol, modifiers)
