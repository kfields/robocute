from crunge import sdl

from robocute.widget.bubble import *

from robocute.message import *
from robocute.robo.message import *

from ..bot import BotBrain

class RoboBrain(BotBrain):
    def __init__(self):
        super().__init__()
        self.bubble = None
        self.on_move = None #callback for camera

    def delete(self):
        self.del_bubble()
        super().delete()
    
    def say(self, items):
        self.del_bubble()
        self.bubble = SpeechBubble(items)
        self.add_bubble(self.bubble)

    def add_bubble(self, bubble):
        coord = self.get_coord()
        t = coord.to_transform()
        t.x += self.node.vu.width
        bubble.set_transform(t)
        self.app.scene.add_bubble(bubble)

    def del_bubble(self):
        if self.bubble != None:
            self.app.scene.remove_bubble(self.bubble)
            self.bubble = None
        
    def go(self, msg):
        self.del_bubble()
        #
        if isinstance(msg, GoNorth):
           self.transfer_to(Coord(self.coord.x, self.coord.y + 1))
        elif isinstance(msg, GoEast):
             self.transfer_to(Coord(self.coord.x + 1, self.coord.y))
        elif isinstance(msg, GoSouth):
             self.transfer_to(Coord(self.coord.x, self.coord.y - 1))
        elif isinstance(msg, GoWest):
             self.transfer_to(Coord(self.coord.x - 1, self.coord.y))
        #
        if self.on_move:
            self.on_move()
                     
    def do(self, msg):
        success = True

        if isinstance(msg, GoMessage):
            self.go(msg)

        '''
        if isinstance(msg, Say):
            self.say(msg.text)
        elif isinstance(msg, GoMessage):
            self.go(msg)
        '''

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        if down and not repeat:
            match key:
                case sdl.SDLK_w:
                    self.do(GoNorth())
                case sdl.SDLK_s:
                    self.do(GoSouth())
                case sdl.SDLK_a:
                    self.do(GoWest())
                case sdl.SDLK_d:
                    self.do(GoEast())
