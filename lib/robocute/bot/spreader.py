import bot

from robocute.node import *
from robocute.block.block import GroupBlock
from robocute.map import *

from random import random

from robocute.builder import *

class Spreader(bot.Bot):
    def __init__(self):
        super(Spreader, self).__init__()
        self.brain = SpreaderBrain(self)

class SpreaderBrain(bot.Brain):
    def __init__(self, node):
        super(SpreaderBrain, self).__init__(node)
    def start(self):
        pass
