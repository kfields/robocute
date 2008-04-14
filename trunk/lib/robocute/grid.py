from node import *
from block.block import *

'''
Warning:  Do not import this.  These are hidden implementation classes.
Only scene.py and builder.py should need to import this file.
'''

class Cell(AbstractCell):
    def __init__(self):
        super(AbstractCell, self).__init__()

    def remove_node(self, node):
        top = self[len(self) - 1]
        if(isinstance(top, GroupBlock)):
            top.remove_node(node)
            return
        #else
        self.remove(node)

    def push_node(self, node):
        if(len(self) ==0):
            self.append(node)
            return
        #else
        top = self[len(self) - 1]
        #top is group ... add to group
        if(isinstance(top, GroupBlock)):
            top.add_node(node)
        elif(isinstance(top, Block)):
            #top is block ... push on stack        
            self.append(node)
        #top is person, place or thing
        #pop top, push group, push old top and new node
        else:
            oldTop = self.pop()
            top = GroupBlock()
            top.add_node(oldTop)
            top.add_node(node)
            self.append(top)

class Row(list):
    def __init__(self):
        super(Row, self).__init__()

class Grid(list):
    def __init__(self):
        super(Grid, self).__init__()
