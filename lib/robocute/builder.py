
import node
#note:These imports are necessary for the dynamic loading to work via eval.
from tool.file import *

from block import *
from block.terrain import *
from block.building import *
from block.landscape import *
#
from prop import *
from item import *
from robo.main import *
from bot.treasure import *
from bot.landscape import *

builder_dict = {}

def build_item(item):
    text = item.body
    
    def assign(node, item):
        for assign in item.assignments:
            text = '_build_object.__setattr__("' + assign[0] + '", ' + assign[1] + ')'
            eval(text, None, {'_build_object':node})
    
    if(text == ''):
        return None
    #else
    node = eval(text, None, {'_build_item':item})
    #builder_dct['_build_item'] = item
    #nodes = eval(text, None, builder_dict)
    #wrap if necessary
    #if not isinstance(nodes, list):
    #   nodes = [nodes]
    if item and item.has_assignments():
        assign(node, item)
    #
    return node

def build(app, text, coord, cell, item = None):
    def assign(nodes, item):
        for node in nodes:
            for assign in item.assignments:
                text = '_build_object.__setattr__("' + assign[0] + '", ' + assign[1] + ')'
                eval(text, None, {'_build_object':node})
    
    if(text == ''):
        return None
    #else
    #nodes = eval(text, None, {'_build_item':item})
    builder_dict['_build_item'] = item
    nodes = eval(text, None, builder_dict)
    
    #nodes = eval(text, builder_dict, {'_build_item':item})
    #wrap if necessary
    if not isinstance(nodes, list):
       nodes = [nodes]
    if item and item.has_assignments():
        assign(nodes, item)
    for node in nodes:
        if isinstance(node, Node):
            cell.push_node(node)
        _coord = Coord(coord.x, coord.y, cell.height)
        node.register(app, _coord)
    #
    return node
            
