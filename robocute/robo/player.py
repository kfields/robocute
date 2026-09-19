from robocute.robo import Robo
from robocute.robo.player_brain import PlayerBrain


class RoboCute(Robo):
    def __init__(self, dna=None):
        super().__init__(dna)
        self.brain = self.add_chip(PlayerBrain())


class RoboBoy(Robo):
    def __init__(self, dna=None):
        super().__init__(dna)
        self.brain = self.add_chip(PlayerBrain())


class RoboCatGirl(Robo):
    def __init__(self, dna=None):
        super().__init__(dna)
        self.brain = self.add_chip(PlayerBrain())


class RoboHornGirl(Robo):
    def __init__(self, dna=None):
        super().__init__(dna)
        self.brain = self.add_chip(PlayerBrain())


class RoboPinkGirl(Robo):
    def __init__(self, dna=None):
        super().__init__(dna)
        self.brain = self.add_chip(PlayerBrain())


class RoboPrincessGirl(Robo):
    def __init__(self, dna=None):
        super().__init__(dna)
        self.brain = self.add_chip(PlayerBrain())
