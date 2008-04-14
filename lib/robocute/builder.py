import node

#note:These imports are necessary for the dynamic loading to work via eval.
from block.block import *
from block.terrain import *
from block.building import *
#
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
        
    def produce(self, text, coord, cell, item = None):
        if(text == ''):
            return None
        #else
        #srcNodes = eval(text)
        nodes = eval(text, None, {'_build_item':item})
        #wrap if necessary
        if not isinstance(nodes, list):
           nodes = [nodes]
        if item and item.has_assignments():
            self.assign(nodes, item)
        for node in nodes:
            node.register(self.scene, coord)
            cell.push_node(node)
        #return last
        return node
    
    def assign(self, nodes, item):
        for node in nodes:
            for assign in item.assignments:
                #text = '_build_object.' + assign[0] + ' = ' + assign[1]
                text = '_build_object.__setattr__("' + assign[0] + '", ' + assign[1] + ')'
                eval(text, None, {'_build_object':node})
            
