'''
fixme:import elsewhere and add classes within module itself!
'''
from builder import add_class, add_classes

from block import GroupBlock
add_class(GroupBlock)

from bot.treasure import TreasureBot
add_class(TreasureBot)

from bot.landscape import LandscapeBot
add_class(LandscapeBot)

from tool.file import FileOpener, FileSaver, Helper, Exiter
add_classes([FileOpener, FileSaver, Helper, Exiter])   

from robo.main import Designer, RoboCute, CharacterBoy, CharacterCatGirl
from robo.main import CharacterHornGirl, CharacterPinkGirl, CharacterPrincessGirl
add_classes([Designer, RoboCute, CharacterBoy, CharacterCatGirl])
add_classes([CharacterHornGirl, CharacterPinkGirl, CharacterPrincessGirl])

from block.terrain import TerrainBlock
add_class(TerrainBlock)

from block.building import BuildingBlock
add_class(BuildingBlock)
from block.landscape import LandscapeBlock
add_class(LandscapeBlock)
#
from item import Treasure, Special
add_classes([Treasure, Special])