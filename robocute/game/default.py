
from robocute.game import *
from robocute.catalog import Catalog
import robocute.persist.catalog.ods
from robocute.world import *
from robocute.brain import *
from robocute.scene import *
import robocute.persist.grid.ods

class DefaultWorld(World):
    def __init__(self, app, name, gridRowMax = WORLD_GRID_ROW_MAX, gridColMax = WORLD_GRID_COL_MAX):
        super().__init__(app, name, 12, 12)
        #
        grid = Grid(self.gridRowMax, self.gridColMax, is_template=True)
        #filename = "Default.ods"
        #filename = "Fountain.ods"
        #filename = "Debug.ods"
        #filename = "SpawnDebug.ods"
        #filename = "TreasureDebug.ods"
        #filename = "SpreaderDebug.ods"
        filename = "TreasureTile.ods"
        filename = 'grid/' + filename
        
        rdr = robocute.persist.grid.ods.Reader(filename, self.app, grid)
        rdr.read()
        self.grid_template = grid
        
    def generate_grid(self, x, y):
        #raise Exception()
        grid = self.grid_template.clone()
        return grid

class DefaultGame(Game):
    def __init__(self, app, name):
        super().__init__(app, name)
    
    def create_world(self):
        world = DefaultWorld(self.app, self.name)
        return world
   
    def create_scene(self):
        scene = GameScene(self.world, self.app)
        return scene
    
    def create_catalog(self):
        catalog = Catalog()
        rdr = robocute.persist.catalog.ods.Reader(catalog, 'catalog/Default.ods')
        rdr.read()
        return catalog