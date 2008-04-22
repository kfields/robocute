import bot

from robocute.node import *
from robocute.block.block import GroupBlock
from robocute.map import *

from random import random

from robocute.builder import *

    
class TreasureBot(bot.Bot):
    def __init__(self):
        super(TreasureBot, self).__init__()
        self.brain = TreasureBotBrain(self)

class TreasureBotBrain(bot.Brain):
    def __init__(self, node):
        super(TreasureBotBrain, self).__init__(node)
        
    def start(self):
        map = Map(self.grid.coordX, self.grid.coordY, self.grid.colCount, self.grid.rowCount)
        def callback(coord):
            return self.explore(coord)
        explorer = Explorer(map, callback)
        coord = self.coord
        cell = self.grid.get_cell_at( coord )
        cell.remove_node(self.node)
        explorer.explore(coord.x - map.coordX, coord.y - map.coordY)
        
    def explore(self, coord):
        cell = Cell()
        node = self.grid.get_top_at(coord)
        if not node:
            return cell
        if isinstance(node, GroupBlock):
            return cell        
        if not node.vacancy:
            return cell
        #else
        dstNodes = self.grid.get_cell_at(coord)
        if(not dstNodes):
            return cell
        #
        die = int(random() * 3)
        if die > 0:
            cell.vacancy = True
            return cell
        
        treasure = {
          0 :'GemBlue()',
          1 :'GemGreen()',
          2 :'GemOrange()',
        }[int(random() * 3)]

        self.app.build(treasure, coord, dstNodes)
        #
        cell.vacancy = True
        return cell