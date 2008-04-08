import bot

from robocute.node import *
from robocute.block.block import GroupBlock
from robocute.map import *

from random import random

from robocute.builder import *

class Spreader(bot.Bot):
    def __init__(self):
        super(Spreader, self).__init__()
        self.brain = SpreaderBrain(self)

class SpreaderBrain(bot.Brain):
    def __init__(self, node):
        super(SpreaderBrain, self).__init__(node)
    def start(self):
        pass
    
class TreasureSpreader(Spreader):
    def __init__(self):
        super(TreasureSpreader, self).__init__()
        self.brain = TreasureSpreaderBrain(self)

class TreasureSpreaderBrain(bot.Brain):
    def __init__(self, node):
        super(TreasureSpreaderBrain, self).__init__(node)
        
    def start(self):
        #map = Map(self.scene.width, self.scene.height)
        map = Map(self.scene.col_count, self.scene.row_count)
        #fn = lambda (coord): self.explore(coord[0], coord[1])
        def callback(x, y):
            return self.explore(x, y)
        explorer = Explorer(map, callback)
        coord = self.coord
        nodes = self.scene.get_nodes_at( coord )
        pop_node(nodes, self.node)
        explorer.explore(coord[0], coord[1])
        
    def explore(self, x, y):
        #block = self.scene.get_top_block_at( (x, y) )
        cell = Cell()
        node = self.scene.get_top_at( (x, y) )
        if(not node):#how is this happening?
            return cell
        if(isinstance(node, NilNode)):
            return cell
        if(isinstance(node, GroupBlock)):
            return cell        
        if(not node.has_vacancy()):
            return cell
        #else
        dstNodes = self.scene.get_nodes_at( (x, y) )
        if(not dstNodes):#how is this happening?
            return cell
        treasure = {
          0 :'GemBlue()',
          1 :'GemGreen()',
          2 :'GemOrange()',
        }[int(random() * 3)]

        #push_node(dstNodes, node)
        self.scene.builder.produce(treasure, (x, y), dstNodes)
        #
        cell.vacancy = True
        return cell