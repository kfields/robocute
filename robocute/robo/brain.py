
import robocute.bot.brain
from robocute.widget.bubble import *

from robocute.message import *
from robocute.robo.message import *

class Brain(robocute.bot.brain.Brain):
    def __init__(self, node):
        super().__init__(node)
        self.bubble = None
        self.on_move = None

    def delete(self):
        self.del_bubble()
        super().delete()
    
    def say(self, items):
        self.del_bubble()
        self.bubble = SpeechBubble(items)
        self.add_bubble(self.bubble)

    def add_bubble(self, bubble):
        coord = self.get_coord()
        #t = self.grid.get_top_transform_at(coord)
        t = coord.to_transform()
        t.x += self.node.vu.width
        bubble.set_transform(t)
        self.app.scene.add_bubble(bubble)

    def del_bubble(self):
        if(self.bubble != None):
            self.app.scene.remove_bubble(self.bubble)
            self.bubble = None
        
    def go(self, msg):
        print('go')
        self.del_bubble()
        #
        if(isinstance(msg, GoNorth)):
           self.transfer_to(Coord(self.coord.x, self.coord.y + 1))
        elif(isinstance(msg, GoEast)):
             self.transfer_to(Coord(self.coord.x + 1, self.coord.y))
        elif(isinstance(msg, GoSouth)):
             self.transfer_to(Coord(self.coord.x, self.coord.y - 1))
        elif(isinstance(msg, GoWest)):
             self.transfer_to(Coord(self.coord.x - 1, self.coord.y))
        #
        if(self.on_move):
            self.on_move()
                     
    def do(self, msg):
        #print(msg)
        success = True
        if(isinstance(msg, Say)):
           self.say(msg.text)
        elif(isinstance(msg, GoMessage)):
             self.go(msg)
