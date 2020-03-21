'''
fixme:import elsewhere and add classes within module itself!
'''
dna_dict = {}
class_dict = {}

from robocute.builder import add_class, add_classes

from robocute.block import GroupBlock
add_class(GroupBlock)

from robocute.bot.treasure import TreasureBot
add_class(TreasureBot)

from robocute.bot.landscape import LandscapeBot
add_class(LandscapeBot)

from robocute.tool.file import FileOpener, FileSaver, Helper, Exiter
add_classes([FileOpener, FileSaver, Helper, Exiter])   

from robocute.robo.main import Designer, RoboCute, RoboBoy, RoboCatGirl
from robocute.robo.main import RoboHornGirl, RoboPinkGirl, RoboPrincessGirl
add_classes([Designer, RoboCute, RoboBoy, RoboCatGirl])
add_classes([RoboHornGirl, RoboPinkGirl, RoboPrincessGirl])

from robocute.block.terrain import TerrainBlock
add_class(TerrainBlock)

from robocute.block.building import BuildingBlock
add_class(BuildingBlock)
from robocute.block.landscape import LandscapeBlock
add_class(LandscapeBlock)
#
from robocute.item import Treasure, Special
add_classes([Treasure, Special])