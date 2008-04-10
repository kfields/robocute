
import robocute.brain
from robocute.bubble.bubble import *

from message import *

class Brain(robocute.brain.Brain):
    def __init__(self, node):
        super(Brain, self).__init__(node)
        self.bubble = None
    
    def say(self, items):
        self.del_bubble()
        self.bubble = SpeechBubble(items)
        self.add_bubble(self.bubble)

    def add_bubble(self, bubble):
        coord = self.get_coord()
        t = self.scene.get_node_transform(self.node, coord)
        t.x += self.node.vu.width
        bubble.set_transform(t)
        self.scene.add_bubble(bubble)

    def del_bubble(self):
        if(self.bubble != None):
            self.scene.remove_bubble(self.bubble)
            self.bubble = None
        
    def go(self, msg):
        self.del_bubble()
        #
        if(isinstance(msg, GoNorth)):
           self.scene.transfer(self.node, self.coord, Coord(self.coord.x, self.coord.y + 1))
        elif(isinstance(msg, GoEast)):
             self.scene.transfer(self.node, self.coord, Coord(self.coord.x + 1, self.coord.y))
        elif(isinstance(msg, GoSouth)):
             self.scene.transfer(self.node, self.coord, Coord(self.coord.x, self.coord.y - 1))
        elif(isinstance(msg, GoWest)):
             self.scene.transfer(self.node, self.coord, Coord(self.coord.x - 1, self.coord.y))
        self.on_move()
                     
    def do(self, msg):
        success = True
        if(isinstance(msg, Say)):
           self.say(msg.text)
        elif(isinstance(msg, GoMessage)):
             self.go(msg)
