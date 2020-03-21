
from random import random

import robocute
from robocute.node import *
from robocute.block import GroupBlock
from robocute.map import *
from robocute.builder import build

class LandscapeBot(robocute.bot.Bot):
    def __init__(self, dna = None):
        super().__init__(dna)
        self.brain = LandscapeBotBrain(self)

class LandscapeBotBrain(robocute.bot.Brain):
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
        if node.vacancy: #opposite of treasure bot.
            return cell
        #else
        dstNodes = self.grid.get_cell_at(coord)
        if(not dstNodes):
            return cell
        #
        die = int(random() * 7)
        if die > 0:
            cell.vacancy = True
            return cell
        
        thing = {
          0 :'Rock()',
          1 :'TreeShort()',
          2 :'TreeTall()',
          3 :'TreeUgly()'                              
        }[int(random() * 4)]

        build(self.app, thing, coord, dstNodes)
        #
        cell.vacancy = True
        return cell