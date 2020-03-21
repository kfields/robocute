
from robocute.message import Message

class Transition(Message):
    def __init__(self, key):
        super().__init__()
        self.key = key

class Phase(Message):
    def __init__(self, key):
        super().__init__()
        self.key = key

class Say(Message):
    def __init__(self, text):
        super().__init__()
        self.text = text

class GoMessage(Message):
    def __init__(self):
        super().__init__()
        
class GoNorth(GoMessage):
    def __init__(self):
        super().__init__()
    
class GoEast(GoMessage):
    def __init__(self):
        super().__init__()

class GoSouth(GoMessage):
    def __init__(self):
        super().__init__()

class GoWest(GoMessage):
    def __init__(self):
        super().__init__()
#
class DoBuild(Message):
    def __init__(self, dna):
        super().__init__()
        self.dna = dna

class DoDelete(Message):
    def __init__(self):
        super().__init__()
