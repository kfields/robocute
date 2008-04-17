from user import *

from robocute.mouse import *
from robocute.block.block import *

#pyglet
from pyglet.window import key

class DesignerMouseQuery(MouseQuery):
    def __init__(self, user, events):
        super(DesignerMouseQuery, self).__init__(events)
        self.user = user
        
    def process(self):
        if(len(self.results) == 0):
            return
        #else
        #get last result, highest z
        result = self.results[len(self.results)-1]
        
        if(not isinstance(result.node, Block)):
            return super(DesignerMouseQuery, self).process()
        #else
        event = self.events[0]
        modifiers = event.modifiers
         
        if modifiers & key.MOD_CTRL:
            self.user.avatar.clone_at(result)
        elif  modifiers & key.MOD_SHIFT:
            self.user.avatar.clear_clones()
            self.user.avatar.clone_to(result)
        else:
            self.user.avatar.clear_clones()
            self.user.avatar.transfer_to(result)
        
class Designer(User):
    
    def __init__(self, app):
        super(Designer, self).__init__(app)
        #self.selector = self.avatar
        self.coord = self.avatar.coord

    def create_avatar(self):
        avatar = self.app.create_avatar("Designer()") #avatar is the brain!!!
        return avatar
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            if self.avatar.has_clones():
                self.avatar.clear_clones()
            else:
                sys.exit()
        elif symbol == key.DELETE:
            self.avatar.do(DoDelete())
        elif symbol == key.W:
            self.avatar.do(GoNorth())
            #self.move_to(Coord(self.coord.x, self.coord.y + 1))
        elif symbol == key.D:
            self.avatar.do(GoEast())
            #self.move_to(Coord(self.coord.x + 1, self.coord.y))
        elif symbol == key.S:
            self.avatar.do(GoSouth())
            #self.move_to(Coord(self.coord.x, self.coord.y - 1))
        elif symbol == key.A:
            self.avatar.do(GoWest())
            #self.move_to(Coord(self.coord.x - 1, self.coord.y))
        else:
            super(Designer, self).on_key_press(symbol, modifiers)
                    
    def create_mousequery(self, events):
        return DesignerMouseQuery(self, events)
