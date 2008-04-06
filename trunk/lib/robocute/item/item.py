
from robocute.node import *
from robocute.vu import *
   
class Item(Node):
    def __init__(self):
        super(Item, self).__init__()

class Treasure(Item):
    def __init__(self):
        super(Treasure, self).__init__()
        self.worth = 0

class Gem(Treasure):
    def __init__(self):
        super(Gem, self).__init__()

class GemBlue(Gem):
    def __init__(self):
        super(GemBlue, self).__init__()
        self.name = "Blue Gem"
        self.worth = 5
        self.vu = ImageVu(self, 'Gem Blue.png')

class GemGreen(Gem):
    def __init__(self): #need blank constructor for builder!
        super(GemGreen, self).__init__()
        self.name = "Green Gem"
        self.worth = 10
        self.vu = ImageVu(self, 'Gem Green.png')

class GemOrange(Gem):
    def __init__(self): #need blank constructor for builder!
        super(GemOrange, self).__init__()
        self.name = "Orange Gem"
        self.worth = 15
        self.vu = ImageVu(self, 'Gem Orange.png')
