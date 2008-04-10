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
        map = Map(self.scene.col_count, self.scene.row_count)
        def callback(coord):
            return self.explore(coord)
        explorer = Explorer(map, callback)
        coord = self.coord
        cell = self.scene.get_cell_at( coord )
        cell.remove_node(self.node)
        explorer.explore(coord.x, coord.y)
        
    def explore(self, coord):
        cell = Cell()
        node = self.scene.get_top_at(coord)
        if(not node):#how is this happening?
            return cell
        if(isinstance(node, NilNode)):
            return cell
        if(isinstance(node, GroupBlock)):
            return cell        
        if(not node.has_vacancy()):
            return cell
        #else
        dstNodes = self.scene.get_cell_at(coord)
        if(not dstNodes):#how is this happening?
            return cell
        treasure = {
          0 :'GemBlue()',
          1 :'GemGreen()',
          2 :'GemOrange()',
        }[int(random() * 3)]

        self.scene.builder.produce(treasure, coord, dstNodes)
        #
        cell.vacancy = True
        return cell