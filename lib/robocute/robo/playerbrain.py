
import brain
from robocute.bubble.bubble import *
from robocute.item.item import *
from robocute.block.block import *

from message import *

from pyglet import clock

from random import random
    
class State(object):
    def __init__(self, brain):
        self.brain = brain
        brain.state = self
        self.phase = None
    #same as enter state
    def __call__(self):
        self.do(self.phase)
    def do(self, msg):
        pass
    #
    def i_love_pyweek(self):
        self.brain.do(Say([Text('I '), Image('Heart.png'), Text(' PyWeek!!! ') ]))
    
class StartState(State):
    def __init__(self, brain):
        super(StartState, self).__init__(brain)
        self.phase = Phase('play')
    def do(self, phase):
        result = {
          'enter': lambda : self.enter(),
          'explain': lambda : self.explain(),
          'play': lambda : self.play()
        }[phase.key]()
    def enter(self):
        self.brain.do(Say([Text('Welcome to RoboCute!') ]))
        self.brain.schedule(Phase('explain'), 3.0)
    def explain(self):
        self.brain.do(Say([Text('Click icons to do stuff!') ]))
        self.brain.schedule(Phase('play'), 3.0)
    def play(self):
        fn = lambda : self.brain.schedule(Transition('main'), .5)
        self.brain.do(Say([Text("Let's play!"), Image('icon/lc_browseforward.png', fn) ]))
        
class MainState(State):
    def __init__(self, brain):
        super(MainState, self).__init__(brain)
        self.phase = Phase('enter')
    def do(self, phase):
        result = {
          'enter': lambda : self.enter(),
          'roll': lambda : self.roll()
        }[phase.key]()
    def enter(self):
        self.brain.update_dash()
        self.brain.do(Say([Text('Roll!'), Image('icon/d12_128x128.png', lambda : self.brain.do(Phase('roll'))) ]))
    def roll(self):
        die = int(random() * 12) + 1
        self.brain.die = die
        #fn = lambda : self.brain.schedule(Transition('move'), 1.0)        
        #self.brain.do(Say([Text('You rolled a ' + str(die) + '!'), Image('icon/lc_browseforward.png', fn)]))
        self.brain.do(Say([Text('You rolled a ' + str(die) + '!')]))
        self.brain.schedule(Transition('move'), 2.0)

class MoveState(State):
    def __init__(self, brain):
        super(MoveState, self).__init__(brain)
        self.phase = Phase('enter')
        self.count = 0
    def do(self, phase):
        result = {
          'enter': lambda : self.enter(),
          'move': lambda : self.move()
        }[phase.key]()
    def enter(self):
        self.count = 0
        self.brain.schedule(Phase('move'))
    def move(self):
        self.count += 1
        if(self.count > self.brain.die):
            self.brain.schedule(Transition('land'), 1.)
            return
        #else
        vacancies = self.brain.find_vacancies()
        #
        vacancy = None
        if(not vacancies):#Dead End!!!
            vacancy = self.brain.old_coord
        else:
            vacancy = vacancies[len(vacancies)-1]
        self.brain.move_to(vacancy)
        # 
        self.brain.do(Say([Text(str(self.count)) ]))
        self.brain.schedule(Phase('move'), .5)

class LandState(State):
    def __init__(self, brain):
        super(LandState, self).__init__(brain)
        self.phase = Phase('enter')
        self.treasure = None # temporary holding spot? ...
    def do(self, phase):
        result = {
          'enter': lambda : self.enter(),
          'exit': lambda : self.exit(),
          'take_treasure': lambda : self.take_treasure()
        }[phase.key]()
    def enter(self):
        items = self.brain.search_for_items()
        if(not items):
            self.brain.schedule(Phase('exit'))
            return
        self.brain.take_items(items)
        #only deal with one item per block for now!!!
        node = items[0]
        self.treasure = node 
        self.brain.do(Say([Text('We found a ' + node.name + '!'), node]))
        self.brain.schedule(Phase('take_treasure'), 2.)
    def exit(self):
        self.brain.schedule(Transition('main'))
    def take_treasure(self):
        self.brain.do(Say([Text('Kaching!')]))
        self.brain.worth += self.treasure.worth
        self.brain.update_dash()
        self.brain.schedule(Transition('main'), 1.)
        
        
class PlayerBrain(brain.Brain):
    def __init__(self, node):
        super(PlayerBrain, self).__init__(node)
        self.state = StartState(self)
        self.die = 0
        self.worth = 0 #heh ... total treasure value
        self.dash_bubble = None
        
    def start(self):    
        self.state()
    def schedule(self, msg, seconds = 0):
        if(seconds == 0):
            self.do(msg)
            return
        #else
        clock.schedule_once(lambda dt, *args, **kwargs : self.do(msg), seconds)
        
    def do(self, msg):
        if(isinstance(msg, Phase)):
            self.state.do(msg)
        elif(isinstance(msg, Transition)):
            self.do_transition(msg)
        else:
            super(PlayerBrain, self).do(msg)
            
    def do_transition(self, transition):
        result = {
          'start': lambda : StartState(self),
          'main': lambda : MainState(self),
          'move': lambda : MoveState(self),
          'land': lambda : LandState(self)
        }[transition.key]()()
        
    def find_vacancies(self):
        vacancies = []
        coord = self.coord
        blockY = coord[1] - 1
        #scan bottom up
        while(blockY < coord[1] + 2):
            blockX = coord[0] - 1
            while(blockX < coord[0] + 2):
                vacant = self.filter_coord( (blockX, blockY) )
                block = self.scene.get_top_block_at((blockX, blockY))
                if(not block):
                    vacant = False
                elif(not block.has_vacancy()):
                    vacant = False
                if(vacant):
                    vacancies.append( (blockX, blockY) )
                #
                blockX += 1                    
            #
            blockY += 1
        #
        return vacancies 
        
    def filter_coord(self, coord):
        #filter out current coord
        if( coord[0] == self.coord[0] and coord[1] == self.coord[1]):
            return False        
        #filter out previous coord
        if( coord[0] == self.old_coord[0] and coord[1] == self.old_coord[1]):
            return False
        #else
        #filter north west
        if( coord[0] == self.coord[0] - 1 and coord[1] == self.coord[1] - 1):
            return False
        #filter north east
        if( coord[0] == self.coord[0] - 1 and coord[1] == self.coord[1] + 1):
            return False
        #filter south east
        if( coord[0] == self.coord[0] + 1 and coord[1] == self.coord[1] + 1):
            return False
        #filter south west
        if( coord[0] == self.coord[0] - 1 and coord[1] == self.coord[1] + 1):
            return False
        #else
        return True
        
    def move_to(self, newCoord):
       self.del_bubble()
       self.scene.transfer(self.node, self.coord, [newCoord[0], newCoord[1]]) #hmmm...
       self.on_move()
       
    def search_for_items(self):
        block = self.scene.get_top_block_at(self.coord) #f6:shorten this?
        if(not isinstance(block, GroupBlock)):
            return None
        nodes = block.nodes
        result = []
        for node in nodes:
            if(isinstance(node, Item)):
                result.append(node)
        return result
        
    def take_items(self, items):
        #if we are here then it's automatically a group block. No need to check.
        block = self.scene.get_top_block_at(self.coord)
        nodes = block.nodes
        for item in items:
            nodes.remove(item)
        
    def update_dash(self):
        if(self.dash_bubble):
            self.scene.dash.remove_node(self.brain.dash_bubble) #ugh,ugh
        self.dash_bubble = self.scene.dash.add_node(DashBubble([Image('Mini Chest.png'), Text(str(self.worth))]))
        