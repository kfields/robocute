
from robocute.message import Message

class Message(Message):
    def __init__(self):
        pass

class Transition(Message):
    def __init__(self, key):
        self.key = key

class Phase(Message):
    def __init__(self, key):
        self.key = key

class Say(Message):
    def __init__(self, text):
        self.text = text

class GoMessage(Message):
    def __init__(self):
        pass
        
class GoNorth(GoMessage):
    def __init__(self):
        pass
    
class GoEast(GoMessage):
    def __init__(self):
        pass

class GoSouth(GoMessage):
    def __init__(self):
        pass

class GoWest(GoMessage):
    def __init__(self):
        pass
