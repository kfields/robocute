from robocute.entity import *


class Item(Entity):
    def __init__(self, dna):
        super().__init__(dna)


"""
Treasure
"""


class Treasure(Item):
    def __init__(self, dna):
        super().__init__(dna)
        self.worth = 0
        self.name = dna.title


"""
Special
"""


class Special(Item):
    def __init__(self, dna):
        super().__init__(dna)
        self.name = dna.title
