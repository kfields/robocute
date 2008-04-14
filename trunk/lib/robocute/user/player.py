from user import *

class Player(User):
    def __init__(self, scene):
        super(Player, self).__init__(scene)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            sys.exit()        
        elif symbol == key.R:
            #self.avatar.do(Transition('start'))
            self.avatar.do(Transition('main'))
        elif symbol == key.W:
            self.avatar.do(GoNorth())
        elif symbol == key.D:
            self.avatar.do(GoEast())
        elif symbol == key.S:
            self.avatar.do(GoSouth())
        elif symbol == key.A:
            self.avatar.do(GoWest())
        else:
            super(Player, self).on_key_press(symbol, modifiers)