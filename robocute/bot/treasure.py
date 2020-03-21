
from random import random

import robocute
from robocute.node import *
from robocute.bot import *
from robocute.block import GroupBlock
from robocute.map import *

from robocute.builder import build
    
class TreasureBot(robocute.bot.Bot):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = TreasureBotBrain(self)

class TreasureBotBrain(robocute.bot.Brain):
    def __init__(self, node):
        super().__init__(node)
        
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
          1 :'GemBlue()',
          2 :'GemBlue()',
          3 :'GemBlue()',                              
          4 :'GemGreen()',
          5 :'GemGreen()',
          6 :'GemGreen()',          
          7 :'GemOrange()',
          8 :'GemOrange()',          
          9 :'TreasureChest()'
        }[int(random() * 10)]

        build(self.app, treasure, coord, dstNodes)
        #
        cell.vacancy = True
        return cell