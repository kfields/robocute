
from robocute.message import Message

class Transition(Message):
    def __init__(self, key):
        super().__init__()
        self.key = key

    def __repr__(self):
        return f"Transition({self.key})"
    
class Phase(Message):
    def __init__(self, key):
        super().__init__()
        self.key = key

    def __repr__(self):
        return f"Phase({self.key})"

class Say(Message):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __repr__(self):
        return f"Say({self.text})"
    
class GoMessage(Message):
    def __init__(self):
        super().__init__()
    def __repr__(self):
        return f"GoMessage()"
class GoNorth(GoMessage):
    def __init__(self):
        super().__init__()
    def __repr__(self):
        return f"GoNorth()"
    
class GoEast(GoMessage):
    def __init__(self):
        super().__init__()
    def __repr__(self):
        return f"GoEast()"

class GoSouth(GoMessage):
    def __init__(self):
        super().__init__()
    def __repr__(self):
        return f"GoSouth()"

class GoWest(GoMessage):
    def __init__(self):
        super().__init__()
    def __repr__(self):
        return f"GoWest()"
#
class DoBuild(Message):
    def __init__(self, dna):
        super().__init__()
        self.dna = dna

    def __repr__(self):
        return f"DoBuild({self.dna})"

class DoDelete(Message):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"DoDelete()"
