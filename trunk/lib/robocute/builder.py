import node

#note:These imports are necessary for the dynamic loading to work via eval.
from block.block import *
from block.terrain import *
from block.building import *
#
from prop.prop import *
from item.item import *
from robo.robo import *
from bot.treasure import *
#
from world import Cell
 
        
def build(app, text, coord, cell, item = None):
    def assign(nodes, item):
        for node in nodes:
            for assign in item.assignments:
                #text = '_build_object.' + assign[0] + ' = ' + assign[1]
                text = '_build_object.__setattr__("' + assign[0] + '", ' + assign[1] + ')'
                eval(text, None, {'_build_object':node})
    
    if(text == ''):
        return None
    #else
    #srcNodes = eval(text)
    nodes = eval(text, None, {'_build_item':item})
    #wrap if necessary
    if not isinstance(nodes, list):
       nodes = [nodes]
    if item and item.has_assignments():
        assign(nodes, item)
    for node in nodes:
        cell.push_node(node)        
        _coord = Coord(coord.x, coord.y, cell.height)
        node.register(app, _coord)
    #return last
    return node
            
