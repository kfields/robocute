import node

def pop_node(nodes, node):
    top = nodes[len(nodes) - 1]
    if(isinstance(top, GroupBlock)):
        top.remove_node(node)
        return
    #else
    nodes.remove(node)
    
def push_node(nodes, node):
    if(len(nodes) ==0):
        nodes.append(node)
        return
    top = nodes[len(nodes) - 1]

    #top is group ... add to group
    if(isinstance(top, GroupBlock)):
        top.add_node(node)
    elif(isinstance(top, Block)):
        #top is block ... push on stack        
        nodes.append(node)
    #top is person, place or thing
    #pop top, push group, push old top and new node
    else:
        oldTop = nodes.pop()
        top = GroupBlock()
        top.add_node(oldTop)
        top.add_node(node)
        nodes.append(top)

#note:These imports are necessary for the dynamic loading to work via eval.
from block.block import *
from prop.prop import *
from item.item import *
from robo.robo import *
from bot.spreader import *
    
'''
basically a factory of factories.
'''
class Builder(object):
    
    def __init__(self, scene):
        self.scene = scene
        
    def produce(self, text, coord, dstNodes):
        #fixme:redundant
        if(text == ''):
            node = NilNode()
            node.register(self.scene, coord)
            push_node(dstNodes, node)
            return node
        #else
        srcNodes = eval(text)
        #wrap if necessary
        if(not isinstance(srcNodes, list)):
           srcNodes = [srcNodes]
        for node in srcNodes:
            node.register(self.scene, coord)
            push_node(dstNodes, node)
        #return last
        return node

