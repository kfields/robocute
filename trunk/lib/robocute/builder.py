import node

#note:These imports are necessary for the dynamic loading to work via eval.
from block.block import *
from prop.prop import *
from item.item import *
from robo.robo import *
from bot.spreader import *
#
from grid import *
 
'''
basically a factory of factories.
'''

class Builder(object):
    
    def __init__(self, scene):
        self.scene = scene
        
    def produce(self, text, coord, cell):
        if(text == ''):
            node = NilNode()
            node.register(self.scene, coord)
            cell.push_node(node)
            return node
        #else
        srcNodes = eval(text)
        #wrap if necessary
        if(not isinstance(srcNodes, list)):
           srcNodes = [srcNodes]
        for node in srcNodes:
            node.register(self.scene, coord)
            cell.push_node(node)
        #return last
        return node
